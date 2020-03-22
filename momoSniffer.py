import configparser
import requests
import selenium
from browsermobproxy import Server
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


timeout = 99
loop_count = 10
username = 'Geco333'
password = '31012310'

user_xpath = '//*[@id="username-field"]'
pass_xpath = '//*[@id="password-field"]'
login_button_xpath = '//*[@id="login_form"]/button'
trivia_xpath = '//*[@id="primary-menu"]/nav/a[8]'

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)

for i in range(loop_count):
    try:
        # Enter the webpage.
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.set_page_load_timeout(999)
        driver.delete_all_cookies()
        driver.get('http://games.moomoo.co.il/')

        # Wait for all the relevant elements to load.
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, user_xpath)))
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, pass_xpath)))

        # Enter username and password
        driver.find_element_by_xpath(user_xpath).send_keys(username)
        driver.find_element_by_xpath(pass_xpath).send_keys(password)

        # Find login button and click it.
        driver.find_element_by_xpath(login_button_xpath).click()

        # Wait for the trivia link to become available and click it.
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, trivia_xpath)))
        driver.find_element_by_xpath(trivia_xpath).click()

        # Close page.
        driver.close()

    except selenium.common.exceptions.NoSuchElementException:
        print('Login NoSuchElementException.')
    except selenium.common.exceptions.TimeoutException:
        print('Login TimeoutException.')
    except selenium.common.exceptions.ElementNotInteractableException:
        print('Login ElementNotInteractableException.')
