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
""" Default view for IConfiglet

$Id$
"""
from zope.cachedescriptors.property import Lazy
from zojax.layoutform import Fields, PageletEditForm


class Configlet(PageletEditForm):
    """ configlet view """

    @property
    def label(self):
        return self.context.__title__

    @property
    def description(self):
        return self.context.__description__

    @Lazy
    def fields(self):
        return Fields(self.context.__schema__)
