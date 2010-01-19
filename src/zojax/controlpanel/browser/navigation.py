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


from zojax.content.type.interfaces import IContentContainer
from zojax.controlpanel.interfaces import IConfiglet, IRootConfiglet, ICategory


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
            self.isRoot = True

        self.isRoot = IRootConfiglet.providedBy(context)

        path = []
        parent = context
        while IConfiglet.providedBy(parent):
            path.insert(0, parent)
            parent = parent.__parent__

        self.root, path = path[0], path[1:]

        self.data = self._process(self.root)

    def _process(self, context, level=1, parent=None):
        request = self.request

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
                    'hasSelected': False,
                    'isLink': bool(list(configlet.__schema__)) or \
                                IContentContainer.providedBy(configlet) or \
                                not ICategory.providedBy(configlet),
                    'parent': parent,
                    'configlet': configlet,
                    'level': level}

            if configlet.__id__ == self.context.__id__:
                info['selected'] = True
                info['hasSelected'] = True
                p = parent
                while p is not None:
                    p['hasSelected'] = True
                    if p['cssClass'].endswith(' closed'):
                        p['cssClass'] = p['cssClass'][0:-7]
                    p = p['parent']
            info['cssClass'] = info['selected'] and 'selected' \
                                or ''

            info['items'] = self._process(configlet, level+1, info)

            if not info['hasSelected'] and info['items']:
                info['cssClass'] += ' closed'

            data.append((configlet.__title__, info))

        data.sort()
        data = [info for t, info in data]
        return data
