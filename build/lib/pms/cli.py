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

@cli.command()
def patients():
    """List all patients in a nice table"""
    try:
        data = api.make_authenticated_get("/api/patients")
        if not data:
            click.echo(click.style("No patients found.", fg="yellow"))
            return

        from tabulate import tabulate

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
        click.echo(click.style(f"Error: {e}", fg="red"))

if __name__ == "__main__":
    cli()
