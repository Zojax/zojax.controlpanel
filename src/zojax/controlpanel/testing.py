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
""" setup zojax.controlpanel

$Id$
"""
from zope import component, interface
from zope.app.testing import setup
from zope.annotation.attribute import AttributeAnnotations
from zope.app.component.hooks import getSite, setSite

from zojax.controlpanel import storage, root, interfaces


def setUpControlPanel():
    setup.setUpTraversal()
    setup.setUpSiteManagerLookup()
    
    component.provideAdapter(root.getSettings, name='settings')
    component.provideAdapter(AttributeAnnotations)
    component.provideUtility(root.RootConfiglet(), interfaces.IConfiglet)
    
    component.provideAdapter(storage.getConfigletData)
    component.provideAdapter(storage.getConfigletDataStorage)
    component.provideAdapter(storage.DefaultConfigletDataFactory)
