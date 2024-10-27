

import click
import logging
from config import Config
from services import get_json_data, send_post_data
from parser import DataParser
from models import Base, ItemModel, IndicatorModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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
                author=item.author if item.author is not None else None,
                company_ids=item.company_ids if item.company_ids is not None else [],
                indicator_ids=item.indicator_ids if item.indicator_ids is not None else [],
                is_published=item.is_published if item.is_published is not None else False,
                is_tailored=item.is_tailored if item.is_tailored is not None else False,
                labels=item.labels if item.labels is not None else [],
                langs=item.langs if item.langs is not None else [],
                seq_update=item.seq_update if item.seq_update is not None else 0,
                malware_list=item.malware_list if item.malware_list is not None else [],
            )
            session.add(item_model)
        else:
            # Update existing item fields
            item_model.author = item.author if item.author is not None else item_model.author
            item_model.company_ids = item.company_ids if item.company_ids is not None else item_model.company_ids
            item_model.indicator_ids = item.indicator_ids if item.indicator_ids is not None else item_model.indicator_ids
            item_model.is_published = item.is_published if item.is_published is not None else item_model.is_published
            item_model.is_tailored = item.is_tailored if item.is_tailored is not None else item_model.is_tailored
            item_model.labels = item.labels if item.labels is not None else item_model.labels
            item_model.langs = item.langs if item.langs is not None else item_model.langs
            item_model.seq_update = item.seq_update if item.seq_update is not None else item_model.seq_update
            item_model.malware_list = item.malware_list if item.malware_list is not None else item_model.malware_list

        # Check if indicators is not None before processing
        if item.indicators is not None:
            # Add or update indicators associated with the item
            for indicator in item.indicators:
                # Check if the indicator already exists in the database
                indicator_model = session.query(IndicatorModel).filter_by(id=indicator.id).first()

                if indicator_model is None:
                    # Create new indicator if it does not exist
                    indicator_model = IndicatorModel(
                        id=indicator.id,
                        date_first_seen=indicator.date_first_seen if indicator.date_first_seen is not None else None,
                        date_last_seen=indicator.date_last_seen if indicator.date_last_seen is not None else None,
                        deleted=indicator.deleted if indicator.deleted is not None else False,
                        description=indicator.description if indicator.description is not None else None,
                        domain=indicator.domain if indicator.domain is not None else None,
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

    logger.info("Fetching data from server...")
    json_data = get_json_data(server_url)

    if json_data is None:
        logger.error("Error: Failed to fetch data from the server.")
        return

    logger.info("Parsing and storing data...")
    parser = DataParser(json_data)

    session = Session()
    try:
        save_to_database(parser, session)
        logger.info("Data fetched and stored successfully.")
    except Exception as e:
        session.rollback()
        logger.error(f"Error storing data: {e}")
    finally:
        session.close()


@cli.command('post')
@click.option('--file', '-f', type=click.Path(exists=True), help='Path to the JSON file to be posted')
def post_data(file):
    """Post JSON data or file to the server."""
    server_url = f"{Config.SERVER_URL}/api/v2/add/data"

    if file:
        logger.info(f"Uploading file: {file}")
        if not file.endswith('.json'):
            logger.error("Error: File must be a JSON file.")
            return
        status_code, response = send_post_data(server_url, file=file)
    else:
        logger.info("Posting sample JSON data...")
        sample_data = {"key": "value"}  # Replace with actual data
        status_code, response = send_post_data(server_url, data=sample_data)

    if status_code == 200:
        logger.info("POST request successful.")
        logger.info(response)
    else:
        logger.error("Error: Failed to send POST request.")


if __name__ == "__main__":
    cli()
