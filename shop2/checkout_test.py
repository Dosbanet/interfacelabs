#!/usr/bin/env python3
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re, time

class CheckoutPageTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_checkout_logged_in(self):
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
                check_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-success")))
            finally:
                check_button.click()
                try:
                    confirm = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-primary")))
                finally:
                    addr = driver.find_element_by_id("id_addr")
                    when = driver.find_element_by_id("id_when")
                    mail = driver.find_element_by_id("id_mail")
                    addr.clear()
                    addr.send_keys("Neverhood, Clay St, 3")
                    when.clear()
                    when.send_keys("2018-06-10")
                    mail.clear()
                    mail.send_keys("clmn@nood.com")
                    confirm.click()
                    assert "Success!!!" in driver.page_source

    def test_checkout_logged_out(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/shop_site/checkout/")
        try:
            alert = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "alert-warning")))
        finally:
            assert "You need to be logged in first." in alert.text                    
                    
    def test_checkout_illegal_fields(self):
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
                check_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-success")))
            finally:
                check_button.click()
                try:
                    confirm = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-primary")))
                finally:
                    confirm.click()
                    try:
                        popup = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input:invalid")))
                    finally:
                        pass
                    addr = driver.find_element_by_id("id_addr")
                    when = driver.find_element_by_id("id_when")
                    mail = driver.find_element_by_id("id_mail")
                    addr.clear()
                    addr.send_keys("Neverhood, Clay St, 3")
                    confirm.click()
                    try:
                        popup = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input:invalid")))
                    finally:
                        pass
                    when.clear()
                    when.send_keys("2018-06-10")
                    confirm.click()
                    try:
                        popup = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input:invalid")))
                    finally:
                        pass
                    mail.clear()
                    mail.send_keys("not mail")
                    confirm.click()
                    try:
                        popup = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input:invalid")))
                    finally:
                        pass
                    # Cleaning
                    cart_link = driver.find_element_by_link_text("Cart")
                    cart_link.click()
                    try:
                        list_pos = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//li[@id='list1']/div/div/h3")))
                    finally:
                        result = re.search(r"[0-9]+", list_pos.text)
                        rem_field = driver.find_element_by_xpath("//li[@id='list1']/div/div/form/input[@name='merchnum']")
                        rem_field.clear()
                        rem_field.send_keys(result.group(0))
                        rem_button = driver.find_element_by_xpath("//li[@id='list1']/div/div/form/input[@type='submit']")
                        rem_button.click()

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()