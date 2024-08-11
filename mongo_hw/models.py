"""models"""
from mongoengine import Document
from mongoengine.fields import ReferenceField, ListField, StringField


class Authors(Document):
    """Represents an author with their biographical details.

    This class is used to store information about an author, including their
    full name, date of birth, location of birth, and a brief description.

    Args:
        Document (mongoengine.Document): Inherits from MongoEngine's Document
        class to enable MongoDB document structure.

    Attributes:
        fullname (StringField): The full name of the author. This field is
            required.
        born_date (StringField): The birth date of the author as a string
            (e.g., "January 1, 1900").
        born_location (StringField): The birthplace of the author.
        description (StringField): A brief description or biography of the
            author.
    """
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quotes(Document):
    """Represents a quote associated with an author.

    This class is used to store quotes, along with the tags associated with
    the quote and a reference to the author who said or wrote it.

    Args:
        Document (mongoengine.Document): Inherits from MongoEngine's Document
            class to enable MongoDB document structure.

    Attributes:
        tags (ListField): A list of tags (keywords) associated with the quote.
        author (ReferenceField): A reference to the `Authors` document that
            identifies the author of the quote. This field is required.
        quote (StringField): The text of the quote. This field is required.
    """
    tags = ListField(StringField())
    author = ReferenceField(Authors, required=True)
    quote = StringField(required=True)
