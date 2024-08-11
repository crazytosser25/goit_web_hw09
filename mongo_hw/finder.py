"""Script for finding quotes in a MongoDB database.

This script allows users to search for quotes in a MongoDB database by author
name, by a single tag, or by multiple tags. The database connection parameters
are loaded from environment variables.

Environment Variables:
    user (str): MongoDB username.
    pass (str): MongoDB password.
    db_name (str): Name of the MongoDB database.
    domain (str): Domain or server address of the MongoDB instance.

Modules:
    os: Provides functions to interact with the operating system.
    sys: Provides access to system-specific parameters and functions.
    mongoengine: MongoDB Object-Document Mapper (ODM) for Python.
    dotenv: Loads environment variables from a .env file.
    models: Contains the Authors and Quotes models for MongoDB.

Functions:
    search_by_author(name: str) -> list: Searches for quotes by a specific
    author.
    search_by_tag(tag: str) -> list: Searches for quotes associated with a
    specific tag.
    search_by_tags(tags: list) -> list: Searches for quotes associated with
    any of the specified tags.
    main() -> None: Main function that prompts the user for a search command
    and displays the results.

Execution:
    The script runs in a loop, continuously prompting the user for input until
    they choose to exit.
"""
import os
import sys
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


def search_by_author(name: str) -> list:
    """Searches for quotes by a specific author.

    Args:
        name (str): The full name of the author.

    Returns:
        list: A list of quotes by the author. If no quotes are found, returns
        an empty list.
    """
    author = Authors.objects(fullname=name).first()
    if author:
        quotes = Quotes.objects(author=author)
        return [quote.quote for quote in quotes]
    return []

def search_by_tag(tag: str) -> list:
    """Searches for quotes associated with a specific tag.

    Args:
        tag (str): The tag to search for.

    Returns:
        list: A list of quotes associated with the tag. If no quotes are found,
        returns an empty list.
    """
    quotes = Quotes.objects(tags=tag)
    return [quote.quote for quote in quotes]

def search_by_tags(tags: list) -> list:
    """Searches for quotes associated with any of the specified tags.

    Args:
        tags (list): A list of tags to search for.

    Returns:
        list: A list of quotes associated with any of the tags. If no quotes
        are found, returns an empty list.
    """
    quotes = Quotes.objects(tags__in=tags)
    return [quote.quote for quote in quotes]

def main() -> None:
    """Main function that handles user input and executes search commands.

    This function prompts the user for input in the format `command:argument`
    where the command can be `name`, `tag`, `tags`, or `exit`. It then executes
    the appropriate search function and displays the results, or exits
    the script.

    Commands:
        name:<author_name> - Search for quotes by the specified author.
        tag:<tag> - Search for quotes with the specified tag.
        tags:<tag1,tag2,...> - Search for quotes with any of the specified tags.
        exit - Exit the script.

    Raises:
        SystemExit: When the user issues the `exit` command.
    """
    text = input(
        "Enter command without spaces(name:, tag:, tags:, exit): "
    ).strip()
    try:
        com, arg = text.split(":")
    except ValueError:
        com = text

    match com:
        case "exit":
            print("Bye.")
            sys.exit(0)
        case "name":
            results = search_by_author(arg)
            if results:
                print(f"Quotes of {arg}:")
                for quote in results:
                    print(f"- {quote}")
            else:
                print(f"No quotes of {arg} finded.")
        case "tag":
            results = search_by_tag(arg)
            if results:
                print(f"Quotes for tag {arg}:")
                for quote in results:
                    print(f"- {quote}")
            else:
                print(f"No quotes for tag {arg} finded.")
        case "tags":
            tag_list = arg.split(',')
            results = search_by_tags(tag_list)
            if results:
                print(f"Quotes for tags {arg}:")
                for quote in results:
                    print(f"- {quote}")
            else:
                print(f"No quotes for tags {arg} finded.")
        case _:
            print("Wrong command.")


if __name__ == '__main__':
    while True:
        main()
