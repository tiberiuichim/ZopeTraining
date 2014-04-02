from zope.interface import Interface
from zope.schema import TextLine
from zope.schema import Text


class IBook(Interface):
    title = TextLine(title=u"Title", required=True, default=u"meme")
    author = TextLine(title=u"Author", required=True)
    text = Text(title=u"Text", required=False)


class IBookCollection(Interface):
    title = TextLine(title=u"Title", required=True)
