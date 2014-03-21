from zope.component import getUtility   #getGlobalSiteManager,
from zope.interface import Interface, implements
import e06_overrides as me

class IUtility(Interface):
    pass


class Utility(object):
    implements(me.IUtility)

    def __repr__(self):
        return "<Utility %s>" % self.__class__.__name__


class FirstUtility(Utility):
    pass

class SecondUtility(Utility):
    pass


def demo():
    from zope.configuration.xmlconfig import xmlconfig  #, file
    xmlconfig(open("e06-main.zcml"))
    z = getUtility(me.IUtility)
    assert z.__class__.__name__ == "SecondUtility"

if __name__ == "__main__":
    demo()
