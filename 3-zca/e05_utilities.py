from zope.component import getGlobalSiteManager, getUtility
from zope.interface import Interface, implements
import e05_utilities as me

class IUtility(Interface):
    pass

class Utility(object):
    implements(me.IUtility)

util = Utility()
util.private = "this is private data"


def demo_utilities(load_zcml):
    gsm = getGlobalSiteManager()

    if load_zcml:
        from zope.configuration.xmlconfig import xmlconfig
        fname = __file__[:-3] + '.zcml'
        xmlconfig(open(fname))
    else:
        gsm.registerUtility(util)
        gsm.registerUtility(factory=Utility, name='from_factory')

    other = getUtility(me.IUtility)
    assert other.private == "this is private data"

    util_from_factory = getUtility(me.IUtility, name="from_factory")
    u2 = getUtility(me.IUtility, name="from_factory")

    assert u2 is util_from_factory
    assert id(u2) == id(util_from_factory)
    assert getattr(util_from_factory, 'private', None) == None

    print "Done"

if __name__ == "__main__":
    import sys
    load_zcml = bool(len(sys.argv) > 1 and sys.argv[1] == 'zcml')
    demo_utilities(load_zcml)

