#!/usr/bin/env python3
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

class RegisterPageTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_register_fields_illegal(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/shop_site/register/")
        username = driver.find_element_by_id("id_username")
        password1 = driver.find_element_by_id("id_password1")
        password2 = driver.find_element_by_id("id_password2")
        confirm = driver.find_element_by_class_name("btn-primary")
        username.clear()
        password1.clear()
        password2.clear()
        confirm.click()
        try:
            popup = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input:invalid")))
        finally:
            pass
        username.send_keys("new user")
        confirm.click()
        try:
            popup = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input:invalid")))
        finally:
            pass
        password1.send_keys("unusual")
        confirm.click()
        try:
            popup = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input:invalid")))
        finally:
            pass

    def test_register_username_illegal(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/shop_site/register/")
        username = driver.find_element_by_id("id_username")
        password1 = driver.find_element_by_id("id_password1")
        password2 = driver.find_element_by_id("id_password2")
        confirm = driver.find_element_by_class_name("btn-primary")
        username.clear()
        password1.clear()
        password2.clear()
        username.send_keys("new user")
        password1.send_keys("unusual")
        password2.send_keys("unusual")
        old_page = driver.find_element_by_tag_name('html')
        confirm.click()
        WebDriverWait(driver, 20).until(EC.staleness_of(old_page))
        assert "Enter a valid username." in driver.page_source

    def test_register_unmatching_passwords(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/shop_site/register/")
        username = driver.find_element_by_id("id_username")
        password1 = driver.find_element_by_id("id_password1")
        password2 = driver.find_element_by_id("id_password2")
        confirm = driver.find_element_by_class_name("btn-primary")
        username.clear()
        password1.clear()
        password2.clear()
        username.send_keys("newuser")
        password1.send_keys("unusual")
        password2.send_keys("unusualgsdfsdfsdf")
        old_page = driver.find_element_by_tag_name('html')
        confirm.click()
        WebDriverWait(driver, 20).until(EC.staleness_of(old_page))
        assert "The two password fields didn't match." in driver.page_source

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()