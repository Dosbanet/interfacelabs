#!/usr/bin/env python3
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re, time

class CartPageTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_cart_remove_all_merch(self):
        driver = self.driver
        # Logging in
        driver.get("http://127.0.0.1:8000/shop_site/accounts/login/")
        username = driver.find_element_by_id("id_username")
        password = driver.find_element_by_id("id_password")
        username.clear()
        username.send_keys("patchy")
        password.clear()
        password.send_keys("nopasaran")
        password.send_keys(Keys.RETURN)
        # Buying stuff
        try:
            buy_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@id='merch1']/form/input[@type='submit']")))            
        finally:
            buy_button.click()
            try:
                list_pos = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//li[@id='list1']/div/div/h3")))
            finally:
                result = re.search(r"[0-9]+", list_pos.text)
                rem_field = driver.find_element_by_xpath("//li[@id='list1']/div/div/form/input[@name='merchnum']")
                rem_field.clear()
                rem_field.send_keys(result.group(0))
                rem_button = driver.find_element_by_xpath("//li[@id='list1']/div/div/form/input[@type='submit']")
                old_page = driver.find_element_by_tag_name('html')
                rem_button.click()
                WebDriverWait(driver, 20).until(EC.staleness_of(old_page))
                assert "There's nothing there!" in driver.page_source

    def test_cart_remove_some_merch(self):
        driver = self.driver
        # Logging in
        driver.get("http://127.0.0.1:8000/shop_site/accounts/login/")
        username = driver.find_element_by_id("id_username")
        password = driver.find_element_by_id("id_password")
        username.clear()
        username.send_keys("patchy")
        password.clear()
        password.send_keys("nopasaran")
        password.send_keys(Keys.RETURN)
        # Buying stuff
        try:
            buy_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@id='merch1']/form/input[@type='submit']")))
        finally:
            buy_field = driver.find_element_by_xpath("//div[@id='merch1']/form/input[@type='number']")
            buy_field.clear()
            buy_field.send_keys("2")
            buy_button.click()
            try:
                rem_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//li[@id='list1']/div/div/form/input[@type='submit']")))
            finally:
                old_page = driver.find_element_by_tag_name('html')
                rem_button.click()
                WebDriverWait(driver, 20).until(EC.staleness_of(old_page))
                list_pos = driver.find_element_by_xpath("//li[@id='list1']/div/div/h3")
                result = re.search(r"[0-9]+", list_pos.text)
                assert result.group(0) == "1"
                # Cleaning
                rem_button = driver.find_element_by_xpath("//li[@id='list1']/div/div/form/input[@type='submit']")
                rem_button.click()

    def test_cart_remove_illegal_merch(self):
        driver = self.driver
        # Logging in
        driver.get("http://127.0.0.1:8000/shop_site/accounts/login/")
        username = driver.find_element_by_id("id_username")
        password = driver.find_element_by_id("id_password")
        username.clear()
        username.send_keys("patchy")
        password.clear()
        password.send_keys("nopasaran")
        password.send_keys(Keys.RETURN)
        # Buying stuff
        try:
            buy_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@id='merch1']/form/input[@type='submit']")))            
        finally:
            buy_button.click()
            try:
                rem_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//li[@id='list1']/div/div/form/input[@name='merchnum']")))
            finally:
                rem_field.clear()
                rem_field.send_keys("2")
                rem_button = driver.find_element_by_xpath("//li[@id='list1']/div/div/form/input[@type='submit']")
                rem_button.click()
                try:
                    popup = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input:invalid")))
                finally:
                    pass
                rem_field.clear()
                rem_field.send_keys("abs")
                rem_button.click()
                try:
                    popup = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input:invalid")))
                finally:
                    pass
                rem_field.clear()
                rem_field.send_keys("0")
                rem_button.click()
                try:
                    popup = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input:invalid")))
                finally:
                    pass
                # Clean
                rem_field.clear()
                rem_field.send_keys("1")
                rem_button.click()
                
        
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()