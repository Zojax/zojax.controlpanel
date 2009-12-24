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
""" zojax.controlpanel interfaces

$Id$
"""
from zope import schema, interface
from zope.location.interfaces import ILocation
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('zojax.controlpanel')


class ICategory(interface.Interface):
    """ settings category """


class IRootConfiglet(interface.Interface):
    """ root settings configlet """


class ISystemConfiglet(interface.Interface):
    """This area allows you to configure system."""


class IContentConfiglet(interface.Interface):
    """This area allows you to configure portal content types."""


class IPrincipalsManagement(interface.Interface):
    """ Portal principals related settings """


class IUIConfiguration(interface.Interface):
    """ Portal UI related settings """


class IConfiglet(ILocation):
    """A group of settings."""

    __id__ = schema.TextLine(
        title = u"Id",
        description = u"The id of the configlet.",
        required = True)

    __title__ = schema.TextLine(
        title = u"Title",
        description = u"The title of the configlet used in the UI.",
        required = True)

    __description__ = schema.TextLine(
        title = u"Description",
        description = u"The description of the configlet used in the UI.",
        required = False)

    __schema__ = interface.Attribute('Configlet schema (readonly)')

    def isAvailable():
        """ is configlet available in current site """


class IConfigletData(interface.Interface):
    """ configlet data storage """


class IConfigletDataFactory(interface.Interface):
    """ configlet data factory """


class IConfigletDataStorage(interface.Interface):
    """ container for IConfigletData """
