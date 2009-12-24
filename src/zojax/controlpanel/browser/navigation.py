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
"""

$Id$
"""
from zope.component import queryMultiAdapter
from zope.viewlet.manager import ViewletManagerBase
from zojax.controlpanel.interfaces import IConfiglet, IRootConfiglet


class Navigation(ViewletManagerBase):

    def update(self):
        super(Navigation, self).update()

        context = self.context

        # search configlet
        while not IConfiglet.providedBy(context):
            context = getattr(context, '__parent__', None)
            if context is None:
                break

        if context is not None:
            self.context = context
        else:
            self.data = []
            self.isRoot = True
            return

        self.isRoot = IRootConfiglet.providedBy(context)
        if self.isRoot:
            return

        path = []
        parent = context
        while IConfiglet.providedBy(parent):
            path.insert(0, parent)
            parent = parent.__parent__

        self.root, path = path[0], path[1:]

        self.data = self._process(self.root, path)

    def _process(self, context, path, level=1):
        request = self.request

        if path:
            data = []
            for name, configlet in context.items():
                if not IConfiglet.providedBy(configlet) or \
                        not configlet.isAvailable():
                    continue

                info = {'name': name,
                        'title': configlet.__title__,
                        'icon': queryMultiAdapter(
                             (configlet, request), name='zmi_icon'),
                        'items': (),
                        'selected': False,
                        'configlet': configlet,
                        'level': level}

                if configlet.__id__ == path[0].__id__:
                    info['items'] = self._process(configlet, path[1:], level+1)

                if configlet.__id__ == self.context.__id__:
                    info['selected'] = True
                    info['items'] = self._process(configlet, [configlet], level+1)

                data.append((configlet.__title__, info))

            data.sort()
            data = [info for t, info in data]
            return data

    def render(self):
        if self.isRoot:
            return u''
        else:
            return super(Navigation, self).render()
