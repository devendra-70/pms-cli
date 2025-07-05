import click
from tabulate import tabulate
from datetime import date
from . import api, config

@click.group()
def cli():
    """PMS CLI: Patient Management System"""

@cli.command()
@click.argument("email")
@click.argument("password")
def login(email, password):
    """Login and save token"""
    token = api.login(email, password)
    config.save_token(token, config.get_base_url())
    click.echo(click.style("✅ Login successful!", fg="green"))

@cli.command()
def logout():
    """Clear saved token"""
    config.clear_token()
    click.echo(click.style("🚪 Logged out.", fg="yellow"))

@cli.command()
@click.option("--name", help="Search patients by name")
@click.option("--email", help="Search patients by email")
def patients(name, email):
    """List all patients or search"""
    if name and email:
        click.echo(click.style("❌ Provide only one: --name or --email, not both.", fg="red"))
        return

    try:
        data = api.search_patients(name=name) if name else \
            api.search_patients(email=email) if email else \
                api.make_authenticated_get("/api/patients")

        if not data:
            click.echo(click.style("No patients found.", fg="yellow"))
            return

        table = []
        for p in data:
            table.append([
                p.get("id"),
                p.get("name"),
                p.get("email"),
                p.get("address"),
                p.get("dateOfBirth")
            ])
        headers = ["ID", "Name", "Email", "Address", "DOB"]
        click.echo(tabulate(table, headers, tablefmt="fancy_grid"))

    except Exception as e:
        click.echo(click.style(f"❌ Error: {e}", fg="red"))

@cli.command("add-patient")
def add_patient():
    """Add a new patient interactively"""
    name = click.prompt("Name")
    email = click.prompt("Email")
    address = click.prompt("Address")
    dob = click.prompt("Date of Birth (YYYY-MM-DD)")
    registered_date = date.today().strftime("%Y-%m-%d")

    payload = {
        "name": name,
        "email": email,
        "address": address,
        "dateOfBirth": dob,
        "registeredDate": registered_date
    }

    click.echo(f"📅 Auto-registered date: {registered_date}")

    try:
        data = api.make_authenticated_post("/api/patients", payload)
        click.echo(click.style(f"✅ Patient added: {data}", fg="green"))
    except Exception as e:
        click.echo(click.style(f"❌ Error: {e}", fg="red"))

@cli.command("update-patient")
@click.option("--email", required=True, help="Patient email to update")
def update_patient(email):
    """Update a patient by email"""
    patient = api.get_patient_by_email(email)
    if not patient:
        click.echo(click.style(f"❌ No patient found with email: {email}", fg="red"))
        return

    click.echo(click.style("\nℹ️ Leave any field blank to KEEP it same.", fg="cyan"))
    click.echo(f"Current Name: {patient['name']}")
    click.echo(f"Current Address: {patient['address']}")
    click.echo(f"Current Date of Birth: {patient['dateOfBirth']}")
    click.echo(f"Current Email: {patient['email']}")
    click.echo("-" * 50)

    name = click.prompt("New name", default="", show_default=False)
    address = click.prompt("New address", default="", show_default=False)
    dob = click.prompt("New Date of Birth (YYYY-MM-DD)", default="", show_default=False)
    new_email = click.prompt("New email", default="", show_default=False)

    payload = {
        "name": name or patient["name"],
        "address": address or patient["address"],
        "dateOfBirth": dob or patient["dateOfBirth"],
        "email": new_email or patient["email"]
    }

    try:
        updated = api.update_patient_by_email(email, payload)
        click.echo(click.style(f"✅ Patient updated: {updated}", fg="green"))
    except Exception as e:
        click.echo(click.style(f"❌ Error: {e}", fg="red"))


@cli.command("delete-patient")
@click.option("--email", required=True, help="Patient email to delete")
def delete_patient(email):
    """Delete a patient by email"""
    try:
        deleted = api.delete_patient_by_email(email)
        click.echo(click.style(f"✅ Deleted patient with ID: {deleted['deleted_id']}", fg="green"))
    except ValueError as ve:
        click.echo(click.style(f"❌ {ve}", fg="red"))
    except Exception as e:
        click.echo(click.style(f"❌ Error: {e}", fg="red"))


@cli.command("delete-patient")
@click.option("--email", required=True, help="Patient email to identify the patient")
def delete_patient(email):
    """Delete a patient by email"""
    try:
        api.delete_patient_by_email(email)
        click.echo(click.style(f"🗑️ Patient with email {email} deleted.", fg="green"))
    except Exception as e:
        click.echo(click.style(f"❌ Error: {e}", fg="red"))


@cli.command("status")
def status():
    """Show analytics status (added & updated counts)"""
    try:
        data = api.make_authenticated_get("/api/analytics/status")
        click.echo(click.style("📊 Analytics Status:", fg="cyan"))
        click.echo(data)
    except Exception as e:
        click.echo(click.style(f"❌ Error: {e}", fg="red"))

if __name__ == "__main__":
    cli()
