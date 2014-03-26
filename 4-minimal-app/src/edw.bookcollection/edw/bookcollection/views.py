from Products.Five import BrowserView
from edw.bookcollection.app import Book
from edw.bookcollection.interfaces import IBook
from slugify import slugify
from zope.browserpage import ViewPageTemplateFile
from zope.event import notify
from zope.formlib.form import FormFields
from zope.formlib.form import PageAddForm
from zope.formlib.form import PageEditForm
from zope.formlib.form import default_page_template
from zope.lifecycleevent import ObjectCreatedEvent  #, ObjectModifiedEvent


class BookCollectionView(BrowserView):
    pass


class BookView(BrowserView):
    pass


class Form(object):
    template = ViewPageTemplateFile('zpt/form.pt')

    @property
    def form_macros(self):
        return default_page_template(self.context)


class AddBook(Form, PageAddForm):
    form_fields = FormFields(IBook)
    title = "Add a new book"

    def createAndAdd(self, data):
        book = Book()
        book.title = data['title']
        book.author = data['author']
        notify(ObjectCreatedEvent(book))
        id = slugify(u" - ".join((book.author, book.title)))
        self.context._setObject(id, book)
        book.id = id
        self._finished_add = True
        return book

    def nextURL(self):
        return self.context.absolute_url()


class EditBook(Form, PageEditForm):
    form_fields = FormFields(IBook)
    title = "Edit book"


class DeleteBook(BrowserView):
    def __call__(self):
        id = self.context.getId()
        books = self.context.get_root()
        next_url = books.absolute_url()
        del books[id]
        return self.request.RESPONSE.redirect(next_url)
