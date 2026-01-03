#!/usr/bin/env python3
"""
DPDC Prepaid CLI

A command-line interface for interacting with DPDC prepaid electricity accounts.
Provides commands to check balance and get customer information.
"""

import click
import sys
from tabulate import tabulate
from .dpdc import DpdcPrepaid
from . import __version__


def handle_api_error(func):
    """Decorator to handle API errors gracefully."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            click.echo(f"❌ Error: {str(e)}", err=True)
            sys.exit(1)
    return wrapper


@click.group()
@click.version_option(version=__version__, prog_name="dpdc-cli")
def app():
    """
    🔌 DPDC Prepaid CLI

    A command-line tool for managing DPDC prepaid electricity accounts.
    Get real-time balance, consumption data, and customer information.
    """
    pass


@app.command(name="get-balance")
@click.option(
    '--customernumber', '-c',
    type=click.STRING,
    required=True,
    help="DPDC prepaid customer number"
)
@handle_api_error
def get_balance(customernumber):
    """Get current account balance and customer information."""
    click.echo("💰 Fetching account balance...")

    client = DpdcPrepaid(customernumber)
    data = client.get_balance()

    if data:
        click.echo("\n📊 Account Balance & Information:")
        click.echo(tabulate(data, tablefmt="simple"))
    else:
        click.echo("⚠️  No balance data found for this account.")


@app.command(name="get-customer-info")
@click.option(
    '--customernumber', '-c',
    type=click.STRING,
    required=True,
    help="DPDC prepaid customer number"
)
@handle_api_error
def get_customer_info(customernumber):
    """Get detailed customer information."""
    click.echo("👤 Fetching customer information...")

    client = DpdcPrepaid(customernumber)
    data = client.get_customer_info()

    if data:
        click.echo("\n📋 Customer Information:")
        click.echo(tabulate(data, tablefmt="simple"))
    else:
        click.echo("⚠️  No customer data found for this account.")


if __name__ == "__main__":
    app()
