import mongoengine


class Page(mongoengine.EmbeddedDocument):
    """Database page representation."""
    page_num = mongoengine.IntField()
    text = mongoengine.StringField()


class Book(mongoengine.Document):
    """Database book representation."""
    title = mongoengine.StringField(max_length=200)
    author = mongoengine.StringField(max_length=200)
    year = mongoengine.IntField()
    pages = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Page))