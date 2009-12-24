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
""" custom IBreadcrumb implementation for IConfiglet

$Id$
"""
from zope import component, interface
from z3c.breadcrumb.browser import GenericBreadcrumb
from zojax.controlpanel.interfaces import IConfiglet


class ConfigletBreadcrumb(GenericBreadcrumb):
    component.adapts(IConfiglet, interface.Interface)

    @property
    def name(self):
        return self.context.__title__ or self.context.__name__
