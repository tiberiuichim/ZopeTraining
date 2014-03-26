from AccessControl import ClassSecurityInfo #, Unauthorized
from OFS.SimpleItem import SimpleItem
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2Base
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from edw.bookcollection.interfaces import IBook
from edw.bookcollection.interfaces import IBookCollection
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from App.ImageFile import ImageFile


class BookCollection(BTreeFolder2Base, SimpleItem):
    """ A book collection
    """
    implements(IBookCollection)

    meta_type = 'Book Collection'
    security = ClassSecurityInfo()

    title = FieldProperty(IBookCollection['title'])
    master = PageTemplateFile('zpt/master.zpt', globals())

    def get_root(self):
        parent = self
        while not IBookCollection.providedBy(parent):
            parent = getattr(self, 'aq_parent', None)
            if not parent:
                break
        return parent

    styles_css = ImageFile('styles.css', globals())


manage_add_book_collection_html = PageTemplateFile(
    'zpt/book_collection_manage_add', globals())


def manage_add_book_collection(factory, id, REQUEST=None):
    """ Create a new BookCollection object """
    parent = factory.Destination()
    form = (REQUEST.form if REQUEST is not None else {})
    obj = BookCollection()
    obj.title = unicode(form.get('title', id))
    obj._setId(id)
    parent._setObject(id, obj)

    if REQUEST is not None:
        REQUEST.RESPONSE.redirect(parent.absolute_url() + '/manage_workspace')


class Book(SimpleItem):
    """ A book
    """

    implements(IBook)

    meta_type = 'Book'
    security = ClassSecurityInfo()

    title = FieldProperty(IBook['title'])
    author = FieldProperty(IBook['author'])
    text = FieldProperty(IBook['text'])


manage_add_book_html = PageTemplateFile(
    'zpt/book_manage_add', globals())

def manage_add_book(factory, id, REQUEST=None):
    """ Create a new Book object """
    parent = factory.Destination()
    form = (REQUEST.form if REQUEST is not None else {})
    obj = Book()
    obj.title = unicode(form.get('title', id))
    obj._setId(id)
    parent._setObject(id, obj)

    if REQUEST is not None:
        REQUEST.RESPONSE.redirect(parent.absolute_url() + '/manage_workspace')

