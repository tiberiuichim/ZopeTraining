from zope.component import adapts, adapter   #, provideAdapter
from zope.interface import Interface, implementer, implements    #implements, Attribute, alsoImplements,
from zope.component import getGlobalSiteManager


class Image(object):
    data = None

class File(object):
    data = None

class Page(object):
    text = None


def get_image_size(obj):
    # parse image with PIL, extract info from there
    return "100 x 200 px"

def get_file_size(obj):
    # get length of bytes, convert to most appropriate increment
    return "114 Mb"

def get_page_size(obj):
    # get length of page in words
    # convert html to plain text, extract nr of words
    return "130 words"


def demo_nonzca():
    print "=====[ Demo non ZCA ]======="
    img = Image()
    img.data = "PNG..."

    file = File()
    file.data = "binary file content here"

    page = Page()
    page.text = "some text"

    sizes = []

    for obj in [img, file, page]:

        if isinstance(obj, Image):
            sizes += [(obj, get_image_size(obj))]

        if isinstance(obj, File):
            sizes += [(obj, get_file_size(obj))]

        if isinstance(obj, File):
            sizes += [(obj, get_file_size(obj))]

    for obj, size in sizes:
        print obj, size


class ISized(Interface):

    def get_size():
        """ Return human readable size
        """


class ImageSize(object):
    adapts(Image)
    implements(ISized)

    def __init__(self, context):
        self.context = context

    def get_size(self):
        return get_image_size(self.context)

#     /-------------\
# File ->  FileSize ->  ISized

@implementer(ISized)
@adapter(File)
class FileSize(object):

    def __init__(self, context):
        self.context = context

    def get_size(self):
        return get_file_size(self.context)


@implementer(ISized)
@adapter(Page)
class PageSize(object):

    def __init__(self, context):
        self.context = context

    def get_size(self):
        return get_page_size(self.context)

gsm = getGlobalSiteManager()
gsm.registerAdapter(ImageSize)
gsm.registerAdapter(FileSize)
gsm.registerAdapter(PageSize)


getToolByName(context, 'portal_catalog')

context.portal_catalog
context.header

context.aq_parent
context.aq_self

context.__name__
context.__parent__


context.se.themes.data_and_maps

context.getSite().portal_catalog

getUtility(ICatalog, context=context)
getMultiAdapter((context, request), name=header).


registry = {
    Image:ImageSize,
    Page:PageSize,
}

def demo_single_adapters():
    print "=====[ Demo single adapters ]======="
    img = Image()
    img.data = "PNG..."

    file = File()
    file.data = "binary file content here"

    page = Page()
    page.text = "some text"

    sizes = [(obj, ISized(obj).get_size())
                    for obj in (img, file, page)]

    for obj, size in sizes:
        print obj, size


if __name__ == "__main__":
    demo_nonzca()
    demo_single_adapters()
    import pdb; pdb.set_trace()





IDublinCore(someobj).modified


class IDublinCore(Interface):
    """
    """

class SomeObj(Persistent):
    data_modificarii = datetime.now()


@adapter(SomeObj)
@implementer(IDublinCore)
class SomeObjDublinCore(object):
    def __init__(self, context):
        self.context = context

    @property
    def modified(self):
        return self.context.data_modificarii


<adapter factory=".SomeObjDublinCore" for="SomeObj" provides="IDublinCore" />
