import os
import pytest
from dotenv import load_dotenv
from selene.support.shared import browser
from framework.demoqa_with_env import DemoQaWithEnv

load_dotenv()


def pytest_addoption(parser):
    parser.addoption("--env")


@pytest.fixture(scope='session')
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope='session')
def demoshop(env):
    return DemoQaWithEnv(env).demoqa


@pytest.fixture(scope='session')
def reqres(env):
    return DemoQaWithEnv(env).reqres


@pytest.fixture
def browser_auth(demoshop):
    browser.config.base_url = "https://demowebshop.tricentis.com/"
    response = demoshop.post("login", json=

    {
        "Email": os.getenv("EMAIL"),
        "Password": os.getenv("PASSWORD")
    },
                             allow_redirects=False
                             )
    auth_cookie = response.cookies.get("NOPCOMMERCE.AUTH")

    browser.open("Themes/DefaultClean/Content/images/star-x-active.png")
    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": auth_cookie})
    return browser
