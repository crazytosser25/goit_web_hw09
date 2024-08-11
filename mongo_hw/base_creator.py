"""Script to create and populate a MongoDB database with authors and quotes.

This script connects to a MongoDB database using credentials stored in
environment variables, loads data from JSON files, and populates the database
with author and quote records.

Environment Variables:
    user (str): MongoDB username.
    pass (str): MongoDB password.
    db_name (str): Name of the MongoDB database.
    domain (str): Domain or server address of the MongoDB instance.

Modules:
    os: Provides functions to interact with the operating system.
    json: Provides functions for parsing JSON data.
    mongoengine: MongoDB Object-Document Mapper (ODM) for Python.
    dotenv: Loads environment variables from a .env file.
    models: Contains the Authors and Quotes models for MongoDB.

Functions:
    load_authors: Loads author data from a JSON file and saves it to the dbase.
    load_quotes: Loads quote data from a JSON file and saves it to the database.

Execution:
    The script will execute the `load_authors` and `load_quotes` functions when
    run directly.
"""
import os
import json
from mongoengine import connect
from dotenv import load_dotenv
from models import Authors, Quotes
# pylint: disable=no-member


load_dotenv()
mongo_user = os.getenv('user')
mongodb_pass = os.getenv('pass')
db_name = os.getenv('db_name')
domain = os.getenv('domain')

connect(
    host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}"""
)


def load_authors() -> None:
    """Loads author data from a JSON file and stores it in the database.

    This function reads the 'authors.json' file, checks if each author already
    exists in the database, and if not, creates a new record for the author
    with the provided details (full name, birth date, birth location, and
    description).

    Raises:
        FileNotFoundError: If the 'authors.json' file is not found.
        json.JSONDecodeError: If the JSON file contains invalid JSON.
    """
    with open('authors.json', 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            author = Authors.objects(fullname=author_data['fullname']).first()
            if not author:
                author = Authors(
                    fullname=author_data['fullname'],
                    born_date=author_data.get('born_date'),
                    born_location=author_data.get('born_location'),
                    description=author_data.get('description')
                )
                author.save()
                print(f'Author {author.fullname} created.')
            else:
                print(f'Author {author.fullname} already exists.')

def load_quotes() -> None:
    """Loads quote data from a JSON file and stores it in the database.

    This function reads the 'quotes.json' file, checks if the author of each
    quote exists in the database, and if so, creates a new record for the quote,
    associating it with the corresponding author.

    Raises:
        FileNotFoundError: If the 'quotes.json' file is not found.
        json.JSONDecodeError: If the JSON file contains invalid JSON.
        Exception: If an author is not found for a given quote.
    """
    with open('quotes.json', 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author_name = quote_data['author']
            author = Authors.objects(fullname=author_name).first()
            if author:
                quote = Quotes(
                    quote=quote_data['quote'],
                    author=author,
                    tags=quote_data.get('tags', [])
                )
                quote.save()
                print(
                    f'Quote "{quote.quote}" by {quote.author.fullname} saved.'
                )
            else:
                print(
                    f'No author {author_name} for quote: {quote_data["quote"]}.'
                )


if __name__ == '__main__':
    load_authors()
    load_quotes()
