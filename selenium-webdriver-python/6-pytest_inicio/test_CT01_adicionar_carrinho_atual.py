import time

import conftest
import pytest

# "from selenium import webdriver" nao é mais necessário importar o webdriver,
# pois ele já está sendo importado no conftest.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@pytest.mark.usefixtures("setup_teardown")
class TestCT01:
    def test_ct01_adicionar_carrinho(self):
        driver = conftest.driver
        # tela de login
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)
        # encontrando o produto e adicionando ao carrinho
        driver.find_element(
            By.XPATH,
            "//*[@class='inventory_item_name ' and text() = 'Sauce Labs Backpack']",
        ).click()
        # adicioinando o produto ao carrinho e validando se o mesmo foi adicionado
        driver.find_element(By.XPATH, "//*[text()='Add to cart']").click()
        driver.find_element(By.XPATH, "//*[@class='shopping_cart_link']").click()
        assert driver.find_element(
            By.XPATH, "//*[@class='inventory_item_name']"
        ).is_displayed()

        # continuando a compra e validando se o produto foi adicionado ao carrinho
        driver.find_element(By.ID, "continue-shopping").click()

        driver.find_element(
            By.XPATH,
            "//*[@class='inventory_item_name ' and text() = 'Sauce Labs Bike Light']",
        ).click()
        driver.find_element(By.XPATH, "//*[text()='Add to cart']").click()
        driver.find_element(By.XPATH, "//*[@class='shopping_cart_link']").click()
        assert driver.find_element(
            By.XPATH, "//*[@class='inventory_item_name']"
        ).is_displayed()
        assert driver.find_element(
            By.XPATH, "//*[@class='inventory_item_name']"
        ).is_displayed()
        time.sleep(2)
        driver.quit()
