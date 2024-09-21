import os
from django.test import TestCase, LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings
from playwright.sync_api import sync_playwright


class AccountsTestCase(StaticLiveServerTestCase):
    def setUp(self):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()

    def tearDown(self):
        # Close the browser after tests
        self.browser.close()
        self.playwright.stop()

    def test_users_can_login(self):
        self.page.goto(self.live_server_url + "/accounts/login")
