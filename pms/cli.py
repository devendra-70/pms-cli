# pms/cli.py

import click
from . import api, config

@click.group()
def cli():
    """PMS CLI: Patient Management System"""

@cli.command()
@click.argument("username")
@click.argument("password")
def login(username, password):
    """Login and save JWT token"""
    token = api.login(username, password)
    config.save_token(token, config.get_base_url())
    click.echo(click.style("✅ Login successful!", fg="green"))

@cli.command()
def logout():
    """Logout: remove JWT token"""
    config.clear_token()
    click.echo(click.style("🚪 Logged out.", fg="yellow"))

@cli.command()
def patients():
    """Example: list patients"""
    try:
        data = api.make_authenticated_get("/api/patients")
        click.echo(data)
    except Exception as e:
        click.echo(click.style(f"Error: {e}", fg="red"))

if __name__ == "__main__":
    cli()
