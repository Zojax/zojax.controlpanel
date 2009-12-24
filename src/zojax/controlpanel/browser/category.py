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
""" category view

$Id$
"""
from zope import interface
from zope.component import queryMultiAdapter
from zojax.controlpanel.interfaces import ICategory, IConfiglet


class CategoryView(object):

    def update(self):
        super(CategoryView, self).update()

        request = self.request
        context = self.context

        data = self.process(context, request)

        configlets = []
        for info in data:
            info['items'] = self.process(info['configlet'], request)
            if ICategory.providedBy(info['configlet']) and not info['items']:
                continue
            configlets.append(info)
        self.data = configlets

    def process(self, context, request):
        data = []
        for configlet in context.values():
            if not IConfiglet.providedBy(configlet) or \
                    not configlet.isAvailable():
                continue

            info = {'name': configlet.__name__,
                    'title': configlet.__title__,
                    'description': configlet.__description__,
                    'icon': queryMultiAdapter(
                        (configlet, request), name='zmi_icon'),
                    'items': (),
                    'selected': False,
                    'configlet': configlet}

            data.append((configlet.__title__, info))

        data.sort()
        return [info for t, info in data]
