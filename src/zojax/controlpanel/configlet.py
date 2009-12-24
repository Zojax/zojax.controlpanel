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
""" Configlet implementation

$Id$
"""
from zope import schema, interface
from zope.location import Location
from zope.component import getUtility, queryUtility
from zope.security.proxy import removeSecurityProxy
from zope.interface.common.mapping import IEnumerableMapping

from interfaces import IConfiglet, IConfigletData

_marker = object()


class Configlet(Location):
    interface.implements(IConfiglet, IEnumerableMapping)

    def __init__(self, tests=()):
        self.__name__ = self.__id__.rsplit('.', 1)[-1]
        self.__tests__ = tests
        self.__subgroups__ = ()

    @property
    def data(self):
        return IConfigletData(self)

    def isAvailable(self):
        for test in self.__tests__:
            if not test(self):
                return False

        if IConfiglet.providedBy(self.__parent__):
            if not self.__parent__.isAvailable():
                return False

        return True

    def add(self, name):
        if name not in self.__subgroups__:
            self.__subgroups__ = self.__subgroups__ + (name,)

    def remove(self, name):
        if name in self.__subgroups__:
            names = list(self.__subgroups__)
            names.remove(name)
            self.__subgroups__ = tuple(names)

    # implementation of IEnumerableMapping interface
    def __getitem__(self, key):
        obj = self.get(key, _marker)
        if obj is _marker:
            raise KeyError(key)
        return obj

    def get(self, key, default=None):
        id = self.__id__ and self.__id__ + '.' + key or key
        configlet = queryUtility(IConfiglet, id, default)
        if configlet is default:
            return default
        return configlet

    def __contains__(self, key):
        return key in self.keys()

    def keys(self):
        return self.__subgroups__

    def __iter__(self):
        id = self.__id__
        if id:
            id = id + '.'

        for key in self.keys():
            name = id + key
            configlet = queryUtility(IConfiglet, name)
            if configlet is not None:
                yield configlet

    def values(self):
        return [group for id, group in self.items()]

    def items(self):
        id = self.__id__
        if id:
            id = id + '.'

        items = []
        for key in self.keys():
            name = id + key
            configlet = queryUtility(IConfiglet, name)
            if configlet is not None:
                items.append((key, configlet))
        return items

    def __len__(self):
        return len(self.keys())
