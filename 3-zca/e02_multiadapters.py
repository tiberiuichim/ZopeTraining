from zope.interface import Interface, implements
from zope.component import getGlobalSiteManager, getAdapters, queryMultiAdapter


class IPortletManager(Interface):
    pass
class IPortlet(Interface):
    pass


import e02_multiadapters as me

class Image(object):
    implements(Interface)
    data = None

class Page(object):
    implements(Interface)
    text = None

class MultiPageDocument(Page):
    pass

class AbstractPortlet(object):
    implements(me.IPortlet)
    name = ""

    def __repr__(self):
        return "<%s on %s for %s>" % (self.__class__.__name__,
                                      self.manager.name, self.context)

    def __init__(self, manager, context):
        self.manager = manager
        self.context = context

class GenericPortlet(AbstractPortlet):
    pass
class ImagePortlet(AbstractPortlet):
    pass
class PagePortlet(AbstractPortlet):
    pass


class AbstractPortletManager(object):
    implements(me.IPortletManager)

    def __init__(self, name):
        self.name = name

    def get_portlets(self, context=Interface):
        return getAdapters((self, context), me.IPortlet)

    def get_portlet(self, context, name):
        return queryMultiAdapter((self, context), me.IPortlet, name=name)

class PortletManagerLeftColumn(AbstractPortletManager):
    pass
class PortletManagerRightColumn(AbstractPortletManager):
    pass


def register():
    gsm = getGlobalSiteManager()
    gsm.registerAdapter(GenericPortlet,
                        (me.IPortletManager, Interface),
                        name="generic portlet")
    gsm.registerAdapter(ImagePortlet,
                        (me.IPortletManager, me.Image),
                        name="image portlet")


def demo_multiadapters(load_zcml):
    print "=====[ Demo multi adapters ]======="

    if load_zcml:
        from zope.configuration.xmlconfig import xmlconfig
        fname = __file__[:-3] + '.zcml'
        xmlconfig(open(fname))
    else:
        register()

    img = me.Image()
    page = me.Page()
    multi_page = me.MultiPageDocument()

    left_column = PortletManagerLeftColumn('left')

    print list(left_column.get_portlets(img))
    #[(u'generic portlet', <GenericPortlet on left for <__main__.Image object at 0x177fdd0>>),
    # (u'image portlet', <ImagePortlet on left for <__main__.Image object at 0x177fdd0>>)]

    gsm = getGlobalSiteManager()
    gsm.registerAdapter(me.PagePortlet,
                       (me.IPortletManager, me.Page),
                        name="page portlet")

    print list(left_column.get_portlets(page))
    # [(u'generic portlet', <GenericPortlet on left for <__main__.Page object at 0x2652e10>>),
    #  (u'page portlet', <PagePortlet on left for <__main__.Page object at 0x2652e10>>)]

    print list(left_column.get_portlets(multi_page))
    # [(u'generic portlet', <GenericPortlet on left for <__main__.MultiPageDocument object at 0x2652e50>>),
    #  (u'page portlet', <PagePortlet on left for <__main__.MultiPageDocument object at 0x2652e50>>)]

    print list(left_column.get_portlets(img))
    # [(u'generic portlet', <GenericPortlet on left for <__main__.Image object at 0x1200dd0>>),
    #  (u'image portlet', <ImagePortlet on left for <__main__.Image object at 0x1200dd0>>)]


if __name__ == "__main__":
    import sys
    load_zcml = bool(len(sys.argv) > 1 and sys.argv[1] == 'zcml')
    demo_multiadapters(load_zcml)
