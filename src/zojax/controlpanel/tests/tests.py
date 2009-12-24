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
""" zojax Control Panel tests

$Id$
"""
__docformat__ = "reStructuredText"

import os, unittest, doctest
from zope import interface, component
from zope.app.testing import setup, functional
from zope.copypastemove import ObjectCopier
from zope.component.event import objectEventNotify
from zope.location.interfaces import ILocation
from zope.app.component.site import changeSiteConfigurationAfterMove
from zope.app.component.interfaces import ISite
from zope.app.container.interfaces import IObjectMovedEvent
from zope.app.container.contained import dispatchToSublocations

from zojax.controlpanel.configlet import Configlet
from zojax.controlpanel.testing import setUpControlPanel


zojaxControlPanelLayer = functional.ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'zojaxControlPanelLayer', allow_teardown=True)


def setUp(test):
    setup.placefulSetUp(True)

    component.provideAdapter(ObjectCopier)
    component.provideHandler(objectEventNotify)
    component.provideHandler(
        changeSiteConfigurationAfterMove, (ISite, IObjectMovedEvent))
    component.provideHandler(
        dispatchToSublocations, (ILocation, IObjectMovedEvent))

    setUpControlPanel()
    setup.setUpTestAsModule(test, 'zojax.controlpanel.README')


def tearDown(test):
    setup.placefulTearDown()
    setup.tearDownTestAsModule(test)


def test_suite():
    testbrowser = functional.FunctionalDocFileSuite(
        "testbrowser.txt",
        optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)
    testbrowser.layer = zojaxControlPanelLayer

    return unittest.TestSuite((
            testbrowser,
            doctest.DocFileSuite(
                '../README.txt',
                setUp=setUp, tearDown=tearDown,
                optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
            doctest.DocFileSuite(
                'site.txt',
                setUp=setUp, tearDown=tearDown,
                optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
            doctest.DocTestSuite(
                'zojax.controlpanel.storage',
                optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
            doctest.DocTestSuite(
                'zojax.controlpanel.configlettype',
                optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
            ))
