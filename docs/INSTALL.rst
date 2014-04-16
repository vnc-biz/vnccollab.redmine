vnccollab.redmine Installation
------------------------------

The preferred way to install vnccollab.redmine is using zc.buildout and the
plone.recipe.zope2instance recipe to manage your project, you can do this:

* Add ``vnccollab.redmine`` to the list of eggs to install, e.g.: ::

    [buildout]
    ...
    eggs =
        ...
        vnccollab.redmine

* Tell the plone.recipe.zope2instance recipe to install a ZCML slug: ::

    [instance]
    recipe = plone.recipe.zope2instance
    ...
    zcml =
        ${buildout:eggs}
        ...
        vnccollab.redmine-overrides

* Set vnccollab.redmine dependency versions: ::

    [versions]
    collective.js.jqueryui = 1.8.16.8
    plone.app.jquery = 1.7.2
    plone.app.jquerytools = 1.4

* Re-run buildout, e.g. with: ::

    $ ./bin/buildout

You can skip the ZCML slug if you are going to explicitly include the package
from another package's configure.zcml file.

