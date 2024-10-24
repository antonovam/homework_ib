import click
import os
from config import Config
from services import get_json_data, send_post_data
from parser import DataParser
from models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database setup
engine = create_engine(Config.DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


@click.group()
def cli():
    """Main entry point for the client application"""
    pass


@cli.command('get')
def fetch_and_store_data():
    """Fetch JSON data from the server and store it in the database."""
    server_url = f"{Config.SERVER_URL}/api/v2/get/data"

    click.echo("Fetching data from server...")
    json_data = get_json_data(server_url)

    if json_data is None:
        click.echo(click.style("Error: Failed to fetch data from the server.", fg='red'))
        return

    click.echo("Parsing and storing data...")
    parser = DataParser(json_data)

    session = Session()
    try:
        parser.save_to_database(session)
        click.echo(click.style("Data fetched and stored successfully.", fg='green'))
    except Exception as e:
        session.rollback()
        click.echo(click.style(f"Error storing data: {e}", fg='red'))
    finally:
        session.close()


@cli.command('post')
@click.option('--file', '-f', type=click.Path(exists=True), help='Path to the JSON file to be posted')
def post_data(file):
    """Post JSON data or file to the server."""
    server_url = f"{Config.SERVER_URL}/api/v2/add/data"
    if file:
        click.echo(f"Uploading file: {file}")
        if not file.endswith('.json'):
            click.echo(click.style("Error: File must be a JSON file.", fg='red'))
            return
        status_code, response = send_post_data(server_url, file=file)
    else:
        click.echo("Posting sample JSON data...")
        sample_data = {"key": "value"}  # Replace with actual data
        status_code, response = send_post_data(server_url, data=sample_data)

    if status_code == 200:
        click.echo(click.style("POST request successful.", fg='green'))
        click.echo(response)
    else:
        click.echo(click.style("Error: Failed to send POST request.", fg='red'))


if __name__ == "__main__":
    cli()
