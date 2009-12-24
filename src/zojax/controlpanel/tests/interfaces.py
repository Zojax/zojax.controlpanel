##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
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
"""

$Id$
"""
from zope import schema, interface
from zope.app.rotterdam import Rotterdam
from zojax.layoutform.interfaces import ILayoutFormLayer


class IDefaultSkin(ILayoutFormLayer, Rotterdam):
    """ my skin """


class ICategory1(interface.Interface):
    """ test category 1 """


class ICategory2(interface.Interface):
    """ test category 2 """


class IConfiglet1(interface.Interface):

    param1 = schema.TextLine(
        title = u'param1',
        default = u'default param1')

    param2 = schema.Int(
        title = u'param2',
        default = 10)


class IConfiglet2(interface.Interface):

    param1 = schema.TextLine(
        title = u'param1',
        default = u'default param1')

    param2 = schema.Int(
        title = u'param2',
        default = 10)

    param3 = schema.TextLine(
        title = u'param3',
        default = u'default param3')


class IConfiglet3(interface.Interface):
    pass


def notAvailable(*args):
    return False
