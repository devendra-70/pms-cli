import click
from . import api, config

@click.group()
def cli():
    """PMS CLI: Patient Management System"""

@cli.command()
@click.argument("email")
@click.argument("password")
def login(email, password):
    """Login with email and password"""
    token = api.login(email, password)
    config.save_token(token, config.get_base_url())
    click.echo(click.style("✅ Login successful!", fg="green"))

@cli.command()
def logout():
    """Clear saved token"""
    config.clear_token()
    click.echo(click.style("🚪 Logged out.", fg="yellow"))

from tabulate import tabulate

@cli.command()
@click.option("--name", help="Search patients by name")
@click.option("--email", help="Search patients by email")
def patients(name, email):
    """List all patients or search by name/email"""
    if name and email:
        click.echo(click.style("❌ Provide only one: --name or --email, not both.", fg="red"))
        return

    try:
        if name or email:
            data = api.search_patients(name, email)
        else:
            data = api.make_authenticated_get("/api/patients")

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

from datetime import date

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

if __name__ == "__main__":
    cli()
