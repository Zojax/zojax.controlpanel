##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" configlet storage implementation

$Id$
"""
from zope import interface, component, event
from zope.security.proxy import removeSecurityProxy
from zope.location.interfaces import ILocation
from zope.lifecycleevent import ObjectCreatedEvent
from zope.app.container.btree import BTreeContainer
from zope.app.component.hooks import getSite
from zope.app.component.interfaces import ILocalSiteManager
from zope.annotation.interfaces import IAttributeAnnotatable

from interfaces import IConfiglet, IConfigletData, IRootConfiglet
from interfaces import IConfigletDataStorage, IConfigletDataFactory


class ConfigletDataStorage(BTreeContainer):
    interface.implements(IConfigletDataStorage)


class ConfigletData(BTreeContainer):
    """
    >>> data = ConfigletData()

    Simple values saved as object attributes

    >>> data['attr1'] = 'value1'
    >>> data['attr1']
    'value1'

    >>> data.get('attr1')
    'value1'

    >>> getattr(data, 'attr1')
    'value1'

    >>> 'attr1' in data
    False

    >>> del data['attr1']

    >>> getattr(data, 'attr1', None) is None
    True

    >>> data['attr1']
    Traceback (most recent call last):
    ...
    KeyError: 'attr1'


    Locatable objects saved as container items

    >>> class Test(object):
    ...     interface.implements(ILocation)
    ...     __parent__ = __name__ = None

    >>> data['attr2'] = Test()

    >>> data['attr2']
    <zojax.controlpanel.storage.Test ...>

    >>> data.get('attr2')
    <zojax.controlpanel.storage.Test ...>

    >>> hasattr(data, 'attr2')
    False

    >>> 'attr2' in data
    True

    >>> data['attr2'].__parent__ is data
    True

    >>> del data['attr2']

    >>> 'attr2' in data
    False

    >>> data['attr2']
    Traceback (most recent call last):
    ...
    KeyError: 'attr2'


    """

    interface.implements(IConfigletData, IAttributeAnnotatable)

    def get(self, name, default=None):
        if name in self:
            return super(ConfigletData, self).__getitem__(name)

        elif hasattr(self, name):
            return getattr(self, name, default)

        else:
            return default

    def __getitem__(self, name):
        if name in self:
            return super(ConfigletData, self).__getitem__(name)

        elif hasattr(self, name):
            return getattr(self, name)

        raise KeyError(name)

    def __setitem__(self, name, value):
        if ILocation.providedBy(value):
            super(ConfigletData, self).__setitem__(name, value)

            if hasattr(self, name):
                delattr(self, name)

        else:
            setattr(self, name, value)

    def __delitem__(self, name):
        if name in self:
            super(ConfigletData, self).__delitem__(name)

        if hasattr(self, name):
            delattr(self, name)


@component.adapter(IConfiglet)
@interface.implementer(IConfigletData)
def getConfigletData(configlet):
    site = getSite()

    storage = None
    if site is not None:
        storage = IConfigletDataStorage(site.getSiteManager())

    if storage is None:
        return IConfigletDataFactory(configlet)()

    if configlet.__id__ not in storage:
        data = IConfigletDataFactory(configlet)()
        event.notify(ObjectCreatedEvent(data))

        if IRootConfiglet.providedBy(configlet):
            if '__rootconfiglet__' not in storage:
                storage['__rootconfiglet__'] = data
            return storage['__rootconfiglet__']
        else:
            storage[configlet.__id__] = data

    return storage[configlet.__id__]


@component.adapter(ILocalSiteManager)
@interface.implementer(IConfigletDataStorage)
def getConfigletDataStorage(siteManager):
    sm = removeSecurityProxy(siteManager)

    storage = sm.get('controlpanel', None)
    if storage is None or not IConfigletDataStorage.providedBy(storage):
        if storage is not None:
            del sm['controlpanel']

        storage = ConfigletDataStorage()
        event.notify(ObjectCreatedEvent(storage))
        sm['controlpanel'] = storage

        storage = sm['controlpanel']

    return storage


class DefaultConfigletDataFactory(object):
    component.adapts(IConfiglet)
    interface.implements(IConfigletDataFactory)

    def __init__(self, configlet):
        self.configlet = configlet

    def __call__(self, *args, **kw):
        return ConfigletData(*args, **kw)
