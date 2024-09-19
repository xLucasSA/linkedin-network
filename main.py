from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import os
from dotenv import load_dotenv
import asyncio
import time


async def get_linkedin_links() -> pd.DataFrame:
    df = pd.read_excel("Networking Escola da Nuvem.xlsx")

    df = df[df.columns[1:3]]
    df.columns = [col.strip() for col in df.columns]
    df.dropna(inplace=True, axis=0)

    df['HasAdd'] = ""

    return df


def get_element_by_xpath(driver: WebDriver, xpath: str) -> WebElement:
    element = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, xpath)))

    return element


def driver_initialization(hiden: bool=False) -> WebDriver:
    """
    Initialize chome driver. If hiden set to True the browser will operate in background
    """
    options = Options()

    if hiden:
        options.add_argument("--headless")
    
    options.add_argument("--window-size=1366,768")
    driver = WebDriver(options=options)

    return driver


def acess_linkedin(driver: WebDriver) -> None:
    linkedin_url = "https://www.linkedin.com/"

    driver.get(linkedin_url)

    login(driver)
    insert_credentials(driver)


def login(driver: WebDriver) -> None:
    xpath_enter_1 = "/html/body/nav/div/a[1]"
    xpath_enter_2 = "/html/body/nav/div/a[2]"

    enter_button = get_element_by_xpath(driver, xpath_enter_1)

    if enter_button.text != "Entrar":
        enter_button = get_element_by_xpath(driver, xpath_enter_2)
    
    enter_button.click()


def insert_credentials(driver: WebDriver) -> None:
    xpath_login = "/html/body/div[1]/main/div[2]/div[1]/form/div[1]/input"
    xpath_senha = "/html/body/div[1]/main/div[2]/div[1]/form/div[2]/input"
    xpath_login_button_1 = "/html/body/div[1]/main/div[2]/div[1]/form/div[3]/button"
    xpath_login_button_2 = "/html/body/div/main/div[2]/div[1]/form/div[4]/button"

    login_input = get_element_by_xpath(driver, xpath_login)
    login_input.click()
    login_input.send_keys(os.getenv('LINKEDIN_LOGIN'))

    password_input = get_element_by_xpath(driver, xpath_senha)
    password_input.click()
    password_input.send_keys(os.getenv('LINKEDIN_PASSWORD'))

    try:
        login_button = get_element_by_xpath(driver, xpath_login_button_1)

    except IndexError: 
        login_button = get_element_by_xpath(driver, xpath_login_button_2)

    login_button.click()

async def main():
    load_dotenv()
    links = await get_linkedin_links()

    driver = driver_initialization()
    acess_linkedin(driver)

    def connect(profile_url: str, driver: WebDriver):
        xpath_connect = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/button"
        xpath_without_note = "/html/body/div[3]/div/div/div[3]/button[2]"
        "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[1]/button"
        driver.get(profile_url)

        try:
            time.sleep(100)
        except:
            pass

    links['Linkedin'].apply(lambda x: connect(x, driver))


asyncio.run(main())