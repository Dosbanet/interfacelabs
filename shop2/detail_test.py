#!/usr/bin/env python3
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re, time

class DetailPageTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_detail_buy_logged_in(self):
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
            merch_link = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, "Nothing")))            
        finally:
            merch_link.click()
            try:
                buy_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "detail-card")))
            finally:
                buy_button = driver.find_element_by_xpath("//input[@type='submit']")
                buy_button.click()
                try:
                    list_pos = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//li[@id='list1']/div/div/h3")))
                finally:
                    result = re.search(r"[0-9]+", list_pos.text)
                    assert result.group(0) == "1"
                    # Cleaning
                    rem_field = driver.find_element_by_xpath("//li[@id='list1']/div/div/form/input[@name='merchnum']")
                    rem_field.clear()
                    rem_field.send_keys(result.group(0))
                    rem_button = driver.find_element_by_xpath("//li[@id='list1']/div/div/form/input[@type='submit']")
                    rem_button.click()

    def test_detail_buy_logged_out(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/shop_site/details/1/")
        try:
            buy_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "detail-card")))           
        finally:
            buy_button = driver.find_element_by_xpath("//input[@type='submit']")
            buy_button.click()
            try:
                alert = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "alert-warning")))
            finally:
                assert "You need to be logged in first." in alert.text

    def test_buy_illegal_ammount(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/shop_site/details/1/")
        buy_field = driver.find_element_by_xpath("//input[@type='number']")
        buy_field.clear()
        buy_field.send_keys("65535")
        buy_button = driver.find_element_by_xpath("//input[@type='submit']")
        buy_button.click()
        try:
            popup = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input:invalid")))
        finally:
            pass
        buy_field.clear()
        buy_field.send_keys("absd")
        buy_button.click()
        try:
            popup = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input:invalid")))
        finally:
            pass
        buy_field.clear()
        buy_field.send_keys("-1")
        buy_button.click()
        try:
            popup = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input:invalid")))
        finally:
            pass
        
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()