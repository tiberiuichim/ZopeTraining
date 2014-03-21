from zope.component import getGlobalSiteManager, adapter
from zope.component import handle
from zope.component.event import objectEventNotify
from zope.component.interfaces import IObjectEvent
from zope.event import notify
from zope.interface import Interface, implements
import e04_event_handlers as me


class IData(Interface):
    pass


class ISomeEvent(Interface):
    pass


class IObjectModifiedEvent(IObjectEvent):
    pass


class SomeEvent(object):
    implements(me.ISomeEvent)


class ObjectModifiedEvent(object):
    implements(me.IObjectModifiedEvent)

    def __init__(self, object):
        self.object = object


@adapter(me.ISomeEvent)
def handle_some_event(event):
    obj = event.object
    obj.data = 'changed'


@adapter(me.IObjectModifiedEvent)
def handle_object_modified_event(object, event):
    obj = event.object
    obj.data = 'changed'


class Data(object):
    implements(me.IData)
    data = "unchanged"


def demo_events(load_zcml):
    gsm = getGlobalSiteManager()

    if load_zcml:
        from zope.configuration.xmlconfig import xmlconfig
        fname = __file__[:-3] + '.zcml'
        xmlconfig(open(fname))
    else:
        gsm.registerHandler(me.handle_some_event)
        gsm.registerHandler(me.handle_object_modified_event,
                            [me.IData, me.IObjectModifiedEvent])

    obj = me.Data()
    evt = me.SomeEvent()
    evt.object = obj

    if load_zcml:
        notify(evt)
    else:
        handle(evt)

    assert obj.data == 'changed'

    obj.data = 'unchanged'

    if load_zcml:
        notify(me.ObjectModifiedEvent(obj))
    else:
        objectEventNotify(me.ObjectModifiedEvent(obj))

    assert obj.data == 'changed'

    print "Done"

if __name__ == "__main__":
    import sys
    load_zcml = bool(len(sys.argv) > 1 and sys.argv[1] == 'zcml')
    demo_events(load_zcml)
