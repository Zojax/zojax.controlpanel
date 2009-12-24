=============
Control Panel
=============

We can access controlpanel with following url http://localhost/settings/
'setting' name availabel for every ISite object.

Let's demonstrate how we can access controlpanel. 

  >>> from zope import component
  >>> from zope.testbrowser.testing import Browser

  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/settings/")
  Traceback (most recent call last):
  ...
  Unauthorized: settings

  >>> browser.open("http://localhost/settings/system/")
  Traceback (most recent call last):
  ...
  Unauthorized: settings

  >>> browser = Browser()
  >>> browser.addHeader("Authorization", "Basic mgr:mgrpw")
  >>> browser.handleErrors = False

We should have 'System settings' link in ISite actions menu

  >>> browser.open("http://localhost/@@contents.html")
  >>> print browser.contents
  <!DOCTYPE html PUBLIC...
  ...<li><a href="settings/">System settings</a></li>...
  <BLANKLINE>

  >>> browser.getLink('System settings').click()
  >>> print browser.contents
  <!DOCTYPE html PUBLIC...
  ...System settings...
  <BLANKLINE>

Configlet categories, by default only first level of categories is
shown. And only categories that have visible configlets.

  >>> 'Category1' in browser.contents
  False

  >>> 'Category2' in browser.contents
  True

Also controlponal show configlets in toplevel categories

  >>> 'Configlet1' in browser.contents
  True

Category shows only its configlets

  >>> browser.open("http://localhost/settings/category1/")
  >>> print browser.contents
  <!DOCTYPE html PUBLIC...
  ...Category1...
  ...Category 1 area...
  ...There are no configlets in this category...
  <BLANKLINE>

  >>> browser.open("http://localhost/settings/category2/")
  >>> print browser.contents
  <!DOCTYPE html PUBLIC...
  ...Category2...
  ...Category 2 area...
  ...http://localhost/settings/category2/configlet1/...Configlet1...
  ...http://localhost/settings/category2/configlet2/...Configlet2...
  <BLANKLINE>

But it should not show not available configlets.

  >>> 'Configlet3' in browser.contents
  False

By default control panel create edit for each configlet, form name 'index.html'

  >>> browser.getLink('Configlet1').click()
  >>> browser.getControl(name='form.buttons.save').click()
