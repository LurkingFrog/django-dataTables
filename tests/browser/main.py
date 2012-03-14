from time import sleep

from selenium import webdriver
from django.contrib.auth.models import User
from greenphire.web.profile.models import UserProfile

import unittest

__all__ = (
    'SummaryDisplayTest',
)


class SummaryDisplayTest(unittest.TestCase):
    fixtures = ['dolittle.json', ]

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(10)

        self.user = User.objects.get(username="test_admin")
        self.profile = UserProfile.objects.get(user=self.user)

    def tearDown(self):
        sleep(10)
        self.browser.close()

    def test_all(self):
        """
        Because of the slow speed of opening the browser,
        we bundle all the tests in here
        """

        # Login using test_admin
        self.login()

        # Test no admin privileges
        self.no_admin_privileges()

        # Test admin to one program, no study

        # Test admin to multi-program, no study

        # Test admin to multi-program, one study

        # Test admin to multi-program, multi study

        # Test pagination
        return True

    def login(self):
        sel = self.browser

        sel.get('http://127.0.0.1:8084/login/')

        user = sel.find_element_by_id('id_username')
        user.send_keys('test_admin')

        password = sel.find_element_by_id('id_password')
        password.send_keys('test')

        sel.find_element_by_xpath("//button").click()

        # Given access to
        self.assertEqual(sel.current_url, 'http://127.0.0.1:8084/')

    def no_admin_privileges(self):
        sel = self.browser

        self.profile.admin_programs.clear()

        sel.get('http://127.0.0.1:8084/my_admin/')

        # This should redirect back to the search, with a gruel message
        self.assertEqual(sel.current_url, 'http://127.0.0.1:8084/')


if __name__ == '__main__':
    unittest.main()
