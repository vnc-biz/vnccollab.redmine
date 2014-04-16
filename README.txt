.. contents::

vnccollab.redmine
================

Overview
--------

``vnccollab.redmine`` offers plone-redmine integration in the form of
one portlet to access to redmine tickets and a viewlet to view the
associated tickets to the current content.

Installation
------------

Please read INSTALL.txt for details about the installation.

Usage
-----

After installing the package, the User's Personal Information page
is extended with two fields: ``Redmine Username`` and ``Redmine Password``.
These fields are needed to authenticate against the redmine server.

For the viewlet to work, the admin must configure the registry
entry ``vnccollab.redmine.server_url`` with the URL of the redmine server.

``vnccollab.redmine`` offers a portlet ``Redmine: Tickets`` that shows
the tickets the current user can see. This portlet can be added in the
usual way.

Known Issues
------------

Due to the use of plone.app.jquery 1.7.2, there could be some issues with
overlays in Plone 4.2.
