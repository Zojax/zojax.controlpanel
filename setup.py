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
"""Setup for zojax.controlpanel package

$Id$
"""
import sys, os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version='1.5.0'


setup(name = 'zojax.controlpanel',
      version = version,
      description = "Control Panel - userfriendly system control panel.",
      long_description = (
        'Detailed Documentation\n' +
        '======================\n'
        + '\n\n' +
        read('src', 'zojax', 'controlpanel', 'README.txt')
        + '\n\n' +
        read('CHANGES.txt')
        ),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3'],
      author = 'Nikolay Kim',
      author_email = 'fafhrd91@gmail.com',
      url='http://zojax.net/',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'':'src'},
      namespace_packages=['zojax'],
      install_requires = ['setuptools', 'ZODB3',
                          'zope.schema',
                          'zope.interface',
                          'zope.component',
                          'zope.annotation',
                          'zope.security',
                          'zope.location',
                          'zope.publisher',
                          'zope.i18n',
                          'zope.i18nmessageid',
                          'zope.viewlet',
                          'zope.contentprovider',
                          'zope.cachedescriptors',
                          'zope.lifecycleevent',
                          'zope.configuration',
                          'zope.app.publisher',
                          'zope.app.component',
                          'zope.app.security',
                          'zope.app.container',
                          'z3c.traverser',
                          'zojax.layout',
                          'zojax.layoutform',
                          'zojax.resourcepackage',
                          'zojax.jquery.treeview',
                          ],
      extras_require = dict(test=['zope.securitypolicy',
                                  'zope.app.security',
                                  'zope.app.testing',
                                  'zope.app.zcmlfiles',
                                  'zope.app.folder',
                                  'zope.traversing',
                                  'zope.testing',
                                  'zope.testbrowser',
                                  'zojax.autoinclude',
                                  'zojax.security',
                                  ]),
      include_package_data = True,
      zip_safe = False
      )
