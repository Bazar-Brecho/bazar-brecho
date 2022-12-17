import pytest
from django.test import TestCase
from .webdrivers import ChromeWebdriver

HOMEPAGE_TITLE = "BAZAR BRECHO"


# ================ Solution using Django's TestCase (UnitTest) ================
class TestMainPage(TestCase):
    def set_up(self):
        self.webdriver = ChromeWebdriver()

    def test_title(self):
        self.webdriver.open_homepage()
        title = self.webdriver.get_title()
        self.assertEqual(title, HOMEPAGE_TITLE)


# ================ Solution using pytest ================
@pytest.fixture(scope='session')
def webdriver():
    return ChromeWebdriver()


def test_title(webdriver):
    webdriver.open_homepage()
    title = webdriver.get_title()
    assert title == HOMEPAGE_TITLE, f"Page title is {title} and it should be {HOMEPAGE_TITLE}"
