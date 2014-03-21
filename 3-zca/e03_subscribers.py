from zope.component import getGlobalSiteManager
from zope.interface import Interface, implements


class IModifierPlugin(Interface):
    """ Interface for modifier plugins
    """

class IData(Interface):
    pass

import e03_subscribers as me

class MakeUpperCasePlugin(object):
    implements(me.IModifierPlugin)

    def __init__(self, context):
        self.context = context

    def run(self):
        self.context.text = self.context.text.upper()


class MakeBig(object):
    implements(me.IModifierPlugin)

    def __init__(self, context):
        self.context = context

    def run(self):
        self.context.text = self.context.text.replace('a few', 'over 9000').replace("A FEW", "OVER 9000")


class Data(object):
    implements(me.IData)
    text = "We have a few missed opportunities here."

class OtherData(object):
    implements(Interface)
    text = "We have a few missed opportunities here."


def demo_subscribers(load_zcml):
    gsm = getGlobalSiteManager()
    if load_zcml:
        from zope.configuration.xmlconfig import xmlconfig
        fname = __file__[:-3] + '.zcml'
        xmlconfig(open(fname))
    else:
        gsm.registerSubscriptionAdapter(me.MakeUpperCasePlugin, (me.IData,))
        gsm.registerSubscriptionAdapter(me.MakeBig, (Interface,))

    data = me.Data()

    subscribers = gsm.subscribers((data,), me.IModifierPlugin)
    for plugin in subscribers:
        plugin.run()

    print data.text
    # WE HAVE OVER 9000 MISSED OPPORTUNITIES HERE.

    otherdata = me.OtherData()
    subscribers = gsm.subscribers((otherdata,), me.IModifierPlugin)
    for plugin in subscribers:
        plugin.run()

    print otherdata.text
    # We have over 9000 missed opportunities here.

    #print subscribers

if __name__ == "__main__":
    import sys
    load_zcml = bool(len(sys.argv) > 1 and sys.argv[1] == 'zcml')
    demo_subscribers(load_zcml)
