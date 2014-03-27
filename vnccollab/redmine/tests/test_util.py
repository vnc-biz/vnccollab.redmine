from Acquisition import aq_parent

from Products.CMFCore.utils import getToolByName

from vnccollab.redmine.tests.base import FunctionalTestCase
from vnccollab.redmine.util import RedmineUtil
from vnccollab.redmine.tests._mock import initialize as initialize_mock



class UtilsTest(FunctionalTestCase):
    def setUp(self):
        super(UtilsTest, self).setUp()
        self.util = RedmineUtil()

    def test_getIssue(self):
        initialize_mock()
        r = self.util.getIssue(123, include='journals')
        self.assertEqual(r.subject, 'Some subject 1')
        self.assertEqual(r.description, 'some description 1')

    def test_getUser(self):
        initialize_mock()
        u = self.util.getUser(123)
        self.assertEqual(u.firstname, 'Marcin')
        self.assertEqual(u.lastname, 'Staniszczak')
        self.assertEqual(u.mail, 'marcin.staniszczak@vnc.biz')
