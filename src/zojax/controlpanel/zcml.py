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
""" zojax:configlet directive

$Id$
"""
from zope import interface
from zope.schema import getFields
from zope.interface.common.mapping import IEnumerableMapping

from zope.component import queryUtility, getGlobalSiteManager

from zope.component.zcml import utility
from zope.component.interface import provideInterface

from zope.schema.interfaces import IField

from zope.security import checkPermission
from zope.security.zcml import Permission
from zope.security.checker import Checker, CheckerPublic

from zope.configuration import fields
from zope.configuration.exceptions import ConfigurationError

from zope.app.security.protectclass import protectName, protectSetAttribute

from configlet import Configlet
from configlettype import ConfigletType
from interfaces import IConfiglet


class IConfigletDirective(interface.Interface):

    name = fields.PythonIdentifier(
        title = u"Name",
        description = u"Name of the configlet used to access the settings.",
        required = True)

    schema = fields.GlobalInterface(
        title = u"Configlet schema",
        description = u"This attribute specifies the schema of the configlet",
        required = True)

    title = fields.MessageID(
        title = u"Title",
        description = u"Title of the configlet used in UIs.",
        required = True)

    description = fields.MessageID(
        title = u"Description",
        description = u"Description of the configlet used in UIs.",
        required = False)

    class_ = fields.GlobalObject(
        title = u"Class",
        description = u'Custom configlet class',
        required = False)

    provides = fields.Tokens(
        title = u'Provides',
        required = False,
        value_type = fields.GlobalInterface())

    permission = Permission(
        title = u'Permission',
        description = u'Default access permission.',
        required = False)

    tests = fields.Tokens(
        title = u"Tests",
        description = u'Tests for check availability.',
        value_type = fields.GlobalObject(),
        required = False)


class ConfigletDirective(object):

    def __init__(self, _context, name, schema, title,
                 description='', class_=None, provides=(),
                 permission='zojax.Configure', tests=(), install_schema_utility=True):

        ConfigletClass = ConfigletType(
            str(name), schema, class_, title, description)

        for test in tests:
            if not callable(test):
                raise ConfigurationError("Test should be callable.")

        if permission == 'zope.Public':
            configlet = ConfigletClass(tuple(tests))
        else:
            configlet = ConfigletClass((
                PermissionChecker(permission),) + tuple(tests))

        utility(_context, IConfiglet, configlet, name=name)

        if install_schema_utility:
            utility(_context, schema, configlet)

        interface.classImplements(ConfigletClass, schema, *provides)

        self._class = ConfigletClass
        self._context = _context
        self._configlet = configlet
        self._permission = permission

        self.require(_context, permission,
                     interface=(IConfiglet, schema), set_schema=(schema,))
        self.require(_context, CheckerPublic, interface=(IEnumerableMapping,))
        self.require(_context, CheckerPublic, attributes=('isAvailable',))

        _context.action(
            discriminator=('zojax:controlpanel', configlet),
            callable=addSubgroup, args=(configlet,))

    def require(self, _context,
                permission=None, attributes=None, interface=None,
                like_class=None, set_attributes=None, set_schema=None):
        """Require a permission to access a specific aspect"""
        if not (interface or attributes or set_attributes or set_schema):
            raise ConfigurationError("Nothing required")

        if not permission:
            raise ConfigurationError("No permission specified")

        if interface:
            for i in interface:
                if i:
                    self.__protectByInterface(i, permission)

        if attributes:
            self.__protectNames(attributes, permission)

        if set_attributes:
            self.__protectSetAttributes(set_attributes, permission)

        if set_schema:
            for s in set_schema:
                self.__protectSetSchema(s, permission)

    def allow(self, _context, attributes=None, interface=None):
        """Like require, but with permission_id zope.Public"""
        return self.require(_context, self._permission, attributes, interface)

    def __protectByInterface(self, interface, permission_id):
        "Set a permission on names in an interface."
        for n, d in interface.namesAndDescriptions(1):
            self.__protectName(n, permission_id)

        self._context.action(
            discriminator = None,
            callable = provideInterface,
            args = (interface.__module__+'.'+interface.getName(), interface))

    def __protectName(self, name, permission_id):
        "Set a permission on a particular name."
        self._context.action(
            discriminator = ('zojax:controlpanel:protectName',
                             self._class, name, object()),
            callable = protectName,
            args = (self._class, name, permission_id))

    def __protectNames(self, names, permission_id):
        "Set a permission on a bunch of names."
        for name in names:
            self.__protectName(name, permission_id)

    def __protectSetAttributes(self, names, permission_id):
        "Set a permission on a bunch of names."
        for name in names:
            self._context.action(
                discriminator = ('zojax:controlpanel:protectSetAttribute',
                                 self._class, name, object()),
                callable = protectSetAttribute,
                args = (self._class, name, permission_id))

    def __protectSetSchema(self, schema, permission_id):
        "Set a permission on a bunch of names."
        _context = self._context

        for name in schema:
            field = schema[name]
            if IField.providedBy(field) and not field.readonly:
                _context.action(
                    discriminator = ('zojax:controlpanel:protectSetAttribute',
                                     self._class, name, object()),
                    callable = protectSetAttribute,
                    args = (self._class, name, permission_id))

        _context.action(
            discriminator = None,
            callable = provideInterface,
            args = (schema.__module__+'.'+schema.getName(), schema))


def addSubgroup(configlet):
    if '.' in configlet.__id__:
        parentId = configlet.__id__.rsplit('.', 1)[0]
    else:
        parentId = ''

    parent = queryUtility(IConfiglet, parentId)
    if parent is None:
        parent = getGlobalSiteManager().getUtility(IConfiglet, parentId)

    parent.add(configlet.__name__)
    configlet.__parent__ = parent


class PermissionChecker(object):

    def __init__(self, permission):
        self.permission = permission

    def __call__(self, configlet):
        return checkPermission(self.permission, configlet)
