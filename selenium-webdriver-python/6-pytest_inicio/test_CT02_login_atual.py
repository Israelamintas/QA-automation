import time

import conftest
import pytest
from selenium.webdriver.common.by import By


@pytest.mark.usefixtures("setup_teardown")
class TestCT02:
    def test_ct02_login_valido(self):
        driver = conftest.driver
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)
        assert (
            driver.find_element(By.XPATH, "//span[@class='title']").text == "Products"
        )
        driver.quit()
