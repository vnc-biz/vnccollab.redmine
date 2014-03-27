from Products.Five import zcml

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2
from Testing import ZopeTestCase as ztc
from zope.configuration import xmlconfig


class VnccollabRedmineLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    dependencies = [
            'collective.js.jqueryui',
            'collective.customizablePersonalizeForm',
            'vnccollab.common',
            'vnccollab.redmine',]


    def setUpZope(self, app, configurationContext):
        # Load ZCML
        for package in self.dependencies:
            module = __import__(package, fromlist=[''])
            self.loadZCML(package=module)

        import collective.customizablePersonalizeForm
        xmlconfig.includeOverrides(configurationContext,
                'overrides.zcml',
                package=collective.customizablePersonalizeForm)

        for package in self.dependencies:
            z2.installProduct(app, package)

    def setUpPloneSite(self, portal):
        for package in self.dependencies:
            self.applyProfile(portal, package + ':default')

VNCCOLLAB_REDMINE_FIXTURE = VnccollabRedmineLayer()
VNCCOLLAB_REDMINE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(VNCCOLLAB_REDMINE_FIXTURE,),
    name="VnccollabRedmineLayer:Integration"
)
VNCCOLLAB_REDMINE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(VNCCOLLAB_REDMINE_FIXTURE, z2.ZSERVER_FIXTURE),
    name="VnccollabRedmineLayer:Functional"
)
