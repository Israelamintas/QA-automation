import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

driver: WebDriver


@pytest.fixture
def setup_teardown():
    global driver
    driver = webdriver.Edge()
    driver.implicitly_wait(2)
    driver.maximize_window()
    driver.get("https://www.saucedemo.com/")
    # run the test
    yield driver

    # teardown code after the test is completed
    driver.quit()
