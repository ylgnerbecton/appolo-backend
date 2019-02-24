# coding: utf-8
import time, os
from django.conf import settings
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
from selenium import webdriver


class CrawlerUtils(object):
    def __init__(self):
        self.logged = False

        if settings.DEBUG:
            binary = FirefoxBinary('/usr/bin/firefox')
            self.driver = webdriver.Firefox(firefox_binary=binary)
        else:
            os.environ['MOZ_HEADLESS'] = '0'
            # capabilities = webdriver.DesiredCapabilities().FIREFOX
            # capabilities["marionette"] = False
            # binary = FirefoxBinary('/usr/bin/firefox')
            # self.driver = webdriver.Firefox(firefox_binary=binary, capabilities=capabilities)
            profile = webdriver.FirefoxProfile()
            self.driver = webdriver.Firefox(firefox_profile=profile, executable_path='/var/www/Sales-Server/api/geckodriver')

    def goTo(self, url):
        self.driver.get(url)

    def wait_until_hide_element(self, xpath, time=20):
        WebDriverWait(self.driver, time).until_not(EC.element_to_be_clickable((By.XPATH, xpath)))
        return True

    def element_exists(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
            return True
        except:
            return False

    def element_is_clickable(self, xpath):
        try:
            WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            return True
        except:
            return False

    def write_input(self, xpath, value='', ttl=30):
        time.sleep(2)
        WebDriverWait(self.driver, ttl).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        field = self.driver.find_element_by_xpath(xpath)
        field.clear()
        field.send_keys(value)

    def write_select(self, xpath, text):
        time.sleep(3)
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        self.driver.find_element_by_xpath(xpath).click()
        self.driver.find_element_by_xpath('%s/option[text()="%s"]' % (xpath, text)).click()

    def write_select_by_index(self, xpath, index):
        time.sleep(3)
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        self.driver.find_element_by_xpath(xpath).click()
        self.driver.find_element_by_xpath('%s/option[%d]' % (xpath, index)).click()

    def click(self, xpath, ttl=30):
        time.sleep(3)
        WebDriverWait(self.driver, ttl).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        self.driver.find_element_by_xpath(xpath).click()

    def click_multiple(self, css_selector):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
        while True:
            try:
                element = self.driver.find_element_by_css_selector(css_selector)
                element.click()
            except:
                break

    def element_has_value(self, xpath):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        field = self.driver.find_element_by_xpath(xpath)
        return field.get_attribute('value') != ''

    def screenshot(self):
        name = 'berkley/error_%d.png' % time.time()
        self.driver.get_screenshot_as_file(os.path.join(settings.BASE_DIR, '_media/%s' % name))
        return name


