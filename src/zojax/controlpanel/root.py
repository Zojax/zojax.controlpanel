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
""" Root configlet

$Id$
"""
from zope import interface, component
from zope.component import getUtility
from zope.security import checkPermission
from zope.security.interfaces import Unauthorized
from zope.traversing.adapters import DefaultTraversable

from zope.app.component.hooks import getSite
from zope.app.component.interfaces import ISite

from configlet import Configlet
from interfaces import _, IConfiglet, IRootConfiglet, ICategory


class RootConfiglet(Configlet):
    interface.implements(ICategory, IRootConfiglet)

    __id__ = ''
    __name__ = 'settings'
    __title__ = _(u'System settings')
    __description__ = ''
    __schema__ = IRootConfiglet

    def __init__(self):
        self.__subgroups__ = ()

    def isAvailable(self):
        return True

    @property
    def __parent__(self):
        return getSite()


@interface.implementer(interface.Interface)
@component.adapter(ISite, interface.Interface)
def getSettings(site, request):
    if not checkPermission('zojax.Configure', site):
        raise Unauthorized('settings')
    return getUtility(IConfiglet)
