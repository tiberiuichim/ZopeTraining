from Products.Five import BrowserView
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from edw.bookcollection.app import Book, BookCollection
from edw.bookcollection.interfaces import IBook, IBookCollection
from slugify import slugify
from zope.browserpage import ViewPageTemplateFile
from zope.event import notify
from zope.formlib.form import FormFields
from zope.formlib.form import PageAddForm
from zope.formlib.form import PageEditForm
from zope.formlib.form import default_page_template
from zope.lifecycleevent import ObjectCreatedEvent  #, ObjectModifiedEvent
from persistent.interfaces import IPersistent
from zope.browser.interfaces import IAdding


class Page(object):
    master = PageTemplateFile('zpt/master.zpt', globals())

    def get_root(self):
        parent = self.context
        while not IBookCollection.providedBy(parent):
            parent = getattr(parent, 'aq_parent',
                             getattr(parent, '__parent__', None))
            if not parent:
                break

        if not IPersistent.providedBy(parent):
            return self.context

        return parent


class BookCollectionView(BrowserView, Page):
    pass


class BookView(BrowserView, Page):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        import pdb; pdb.set_trace()
        return super(BookView, self).__call__()


class Form(object):
    template = ViewPageTemplateFile('zpt/form.pt')

    @property
    def form_macros(self):
        return default_page_template(self.context)

    def get_context(self):
        if IAdding.providedBy(self.context):
            return self.context.context
        return self.context


class AddBookCollection(Form, Page, PageAddForm):
    form_fields = FormFields(IBookCollection)
    title = "Add a new book collection"

    def createAndAdd(self, data):
        collection = BookCollection()
        collection.title = data['title']
        notify(ObjectCreatedEvent(collection))
        id = slugify(collection.title)
        self.get_context()._setObject(id, collection)
        collection.id = id
        self._finished_add = True
        return collection

    def nextURL(self):
        return self.context.absolute_url()


class AddBook(Form, Page, PageAddForm):
    form_fields = FormFields(IBook)
    title = "Add a new book"

    def createAndAdd(self, data):
        book = Book()
        book.title = data['title']
        book.author = data['author']
        book.text = data['text']
        notify(ObjectCreatedEvent(book))
        id = slugify(u" - ".join((book.author, book.title)))
        self.context._setObject(id, book)
        book.id = id
        self._finished_add = True
        return book

    def nextURL(self):
        return self.context.absolute_url()


class EditBook(Form, Page, PageEditForm):
    form_fields = FormFields(IBook)
    title = "Edit book"


class DeleteBook(BrowserView, Page):
    def __call__(self):
        id = self.context.getId()
        books = self.get_root()
        next_url = books.absolute_url()
        del books[id]
        return self.request.RESPONSE.redirect(next_url)
