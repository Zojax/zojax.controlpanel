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
from zope import interface
from zope.schema import getFields
from zope.component import getUtility
from zojax.layoutform import Fields, PageletEditForm
from zojax.wizard import WizardWithTabs
from zojax.wizard.step import WizardStep, WizardStepForm
from zojax.wizard.button import WizardButton
from zojax.wizard.interfaces import ISaveable, IForwardAction
from zojax.layoutform.interfaces import ISaveAction
from zojax.controlpanel.interfaces import _

from interfaces import IConfigletEditWizard


class ConfigletEditWizard(WizardWithTabs):
    interface.implements(IConfigletEditWizard)

    prefix = 'configlet.'
    id = 'configlet-edit-wizard'

    @property
    def title(self):
        return self.context.__title__

    @property
    def description(self):
        return self.context.__description__


class ConfigletEditStep(WizardStepForm):
    interface.implements(ISaveable)

    name = 'configlet'
    title = _('Configure')
    label = _('Configure configlet')
    permission = 'zope.Public'

    @property
    def fields(self):
        return Fields(self.getContent().__schema__)

    def isAvailable(self):
        if not len(getFields(self.getContent().__schema__)):
            return False

        return super(ConfigletEditStep, self).isAvailable()


next = WizardButton(
    title = _(u'Next'),
    condition = lambda form: not form.isLastStep() \
        and not form.step.isSaveable(),
    weight = 300,
    provides = IForwardAction)

save = WizardButton(
    title = _(u'Save'),
    condition = lambda form: form.step.isSaveable(),
    weight = 400,
    provides = ISaveAction)
