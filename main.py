from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os

def driver_initialization():
    options = Options()
    options.add_argument("--window-size=1366,768")
    driver = webdriver.Chrome(options=options)

    return driver


def acess_linkedin(driver: webdriver):
    linkedin_url = "https://www.linkedin.com/"

    driver.get(linkedin_url)

    login(driver)
    insert_credentials(driver)


def login(driver: webdriver):
    xpath_login = "/html/body/nav/div/a[2]"

    enter_button = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, xpath_login)))
    enter_button.click()


def insert_credentials(driver: webdriver):
    xpath_login = "/html/body/div[1]/main/div[2]/div[1]/form/div[1]/input"
    xpath_senha = "/html/body/div[1]/main/div[2]/div[1]/form/div[2]/input"
    xpath_login_button = "/html/body/div[1]/main/div[2]/div[1]/form/div[3]/button"

    login_input = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, xpath_login)))
    login_input.click()
    login_input.send_keys(os.getenv('LOGIN'))

    password_input = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, xpath_senha)))
    password_input.click()
    password_input.send_keys(os.getenv('PASSWORD'))

    login_button = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, xpath_login_button)))
    login_button.click()


def main():

    driver = driver_initialization()
    acess_linkedin(driver)
    

main()