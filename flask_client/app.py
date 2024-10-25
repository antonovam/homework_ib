import click
from config import Config
from services import get_json_data, send_post_data
from parser import DataParser
from models import Base, ItemModel, IndicatorModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database setup
engine = create_engine(Config.DATABASE_URL)
Base.metadata.drop_all(engine)  # Drops all tables
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def save_to_database(data_parser: DataParser, session):
    """Saves parsed data from DataParser into the database."""
    for item in data_parser.items:
        # Check if the item already exists in the database
        item_model = session.query(ItemModel).filter_by(id=item.id).first()

        if item_model is None:
            # Create new item if it does not exist
            item_model = ItemModel(
                id=item.id,
                author=item.author,
                company_ids=item.company_ids,
                indicator_ids=item.indicator_ids,
                is_published=item.is_published,
                is_tailored=item.is_tailored,
                labels=item.labels,
                langs=item.langs,
                seq_update=item.seq_update,
                malware_list=item.malware_list
            )
            session.add(item_model)
        else:
            # Update existing item fields
            item_model.author = item.author
            item_model.company_ids = item.company_ids
            item_model.indicator_ids = item.indicator_ids
            item_model.is_published = item.is_published
            item_model.is_tailored = item.is_tailored
            item_model.labels = item.labels
            item_model.langs = item.langs
            item_model.seq_update = item.seq_update
            item_model.malware_list = item.malware_list

        # Add or update indicators associated with the item
        for indicator in item.indicators:
            indicator_model = session.query(IndicatorModel).filter_by(id=indicator.id).first()
            if indicator_model is None:
                indicator_model = IndicatorModel(
                    id=indicator.id,
                    date_first_seen=indicator.date_first_seen,
                    date_last_seen=indicator.date_last_seen,
                    deleted=indicator.deleted,
                    description=indicator.description,
                    domain=indicator.domain,
                    item_id=item.id
                )
                session.add(indicator_model)

    session.commit()

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
        save_to_database(parser, session)
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
