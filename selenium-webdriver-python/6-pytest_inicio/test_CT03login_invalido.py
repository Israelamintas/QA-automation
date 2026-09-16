import time

import conftest
import pytest
from selenium.webdriver.common.by import By


@pytest.mark.usefixtures("setup_teardown")
class TestCT03:
    def test_ct03_login_invalido(self):
        driver = conftest.driver
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("zzzzz")
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)
        assert len(driver.find_elements(By.XPATH, "//span[@class='title']")) == 0
        driver.quit()
