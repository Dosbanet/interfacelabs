#!/usr/bin/env python3
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

class LoginPageTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_login_success(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/shop_site/accounts/login/")
        username = driver.find_element_by_id("id_username")
        password = driver.find_element_by_id("id_password")
        username.clear()
        username.send_keys("patchy")
        password.clear()
        password.send_keys("nopasaran")
        password.send_keys(Keys.RETURN)
        try:
            login = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "merch_list")))
        finally:
            assert "patchy" in driver.page_source

    def test_login_logout(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/shop_site/accounts/login/")
        username = driver.find_element_by_id("id_username")
        password = driver.find_element_by_id("id_password")
        username.clear()
        username.send_keys("patchy")
        password.clear()
        password.send_keys("nopasaran")
        password.send_keys(Keys.RETURN)
        try:
            login = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "merch_list")))
        finally:
            logout = driver.find_element_by_link_text("Logout")
            old_page = driver.find_element_by_tag_name('html')
            logout.click()
            WebDriverWait(driver, 20).until(EC.staleness_of(old_page))
            assert "Welcome, new user" in driver.page_source
            
    def test_login_failure(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/shop_site/accounts/login/")
        username = driver.find_element_by_id("id_username")
        password = driver.find_element_by_id("id_password")
        username.clear()
        username.send_keys("not user")
        password.clear()
        password.send_keys("12345")
        password.send_keys(Keys.RETURN)
        try:
            login = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "errorlist")))
        finally:
            assert "Please enter a correct" in driver.page_source
            
    def test_login_name_none(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/shop_site/accounts/login/")
        username = driver.find_element_by_id("id_username")
        password = driver.find_element_by_id("id_password")
        username.clear()
        password.clear()
        password.send_keys("nopasaran")
        password.send_keys(Keys.RETURN)
        try:
            login = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input:invalid")))
        finally:
            pass
    
    def test_login_pass_none(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/shop_site/accounts/login/")
        username = driver.find_element_by_id("id_username")
        password = driver.find_element_by_id("id_password")
        username.clear()
        username.send_keys("patchy")
        password.clear()
        password.send_keys(Keys.RETURN)
        try:
            login = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input:invalid")))
        finally:
            pass
    
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()