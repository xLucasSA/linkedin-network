from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import pandas as pd
import os
from dotenv import load_dotenv
import time
import random


def get_linkedin_links() -> pd.DataFrame:
    df = pd.read_excel("Networking Escola da Nuvem.xlsx")

    df.columns = [col.strip() for col in df.columns]
    df.dropna(inplace=True, axis=0, subset='Linkedin')

    if 'HasAdd' not in df.columns:
        df['HasAdd'] = ""

    return df


def get_element_by_xpath(driver: WebDriver, xpath: str) -> WebElement:
    element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    
    time.sleep(random.uniform(2, 5))

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
    xpath_login_button_3 = "/html/body/div/main/div[2]/div[1]/form/div[3]/button"

    login_input = get_element_by_xpath(driver, xpath_login)
    login_input.click()
    login_input.send_keys(os.getenv('LINKEDIN_LOGIN'))

    password_input = get_element_by_xpath(driver, xpath_senha)
    password_input.click()
    password_input.send_keys(os.getenv('LINKEDIN_PASSWORD'))

    try:
        login_button = get_element_by_xpath(driver, xpath_login_button_1)
        
    except TimeoutException:
        login_button = get_element_by_xpath(driver, xpath_login_button_2)

    if login_button.text != "Entrar":
        try:
            login_button = get_element_by_xpath(driver, xpath_login_button_2)

        except TimeoutException:
            login_button = get_element_by_xpath(driver, xpath_login_button_3)


    login_button.click()


def send_connection_without_text(driver: WebDriver) -> None:
    xpath_without_note = "/html/body/div[3]/div/div/div[3]/button[2]"

    without_note_button = get_element_by_xpath(driver, xpath_without_note)
    without_note_button.click()

    return


def try_connect_direct(driver: WebDriver) -> bool:
    xpath_connect_1 = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/button"
    xpath_connect_2 = "/html/body/div[4]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/button"

    xpaths = [xpath_connect_1, xpath_connect_2]

    for xpath in xpaths:
        try:
            connect_button = get_element_by_xpath(driver, xpath)

            if connect_button.text == "Pendente":
                return True
            
            if connect_button.text == "Seguir":
                continue
            
            connect_button.click()

            send_connection_without_text(driver)

            return True
        
        except TimeoutException:
            continue

    return False

def try_connect_with_more_options(driver: WebDriver) -> bool:
    xpath_more = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/button"
    xpath_more_connect = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/div/div/ul/li[3]/div"

    more_button = get_element_by_xpath(driver, xpath_more)
    more_button.click()

    connect_button = get_element_by_xpath(driver, xpath_more_connect)
    
    if connect_button.text != "Conectar":
        return False
    
    connect_button.click()

    send_connection_without_text()

    return True


def have_add(driver: WebDriver) -> bool:
    connected = try_connect_direct(driver)
    if connected:
        return True
    
    connected = try_connect_with_more_options(driver)
    if connected:
        return True
    
    return True


def connect(profile_url: str, driver: WebDriver) -> str:
    try:
        driver.get(profile_url)
    except:
        return "X"

    return "X" if have_add(driver) else ""


def main():
    load_dotenv()
    links = get_linkedin_links()

    driver = driver_initialization(hiden=False) #turn to True to run in background
    acess_linkedin(driver)

    added = 0
    limit = 8
    for index, row in links.iterrows():

        if row['HasAdd'] == "X":
            continue
        
        links.at[index, 'HasAdd'] = connect(row['Linkedin'], driver)

        if links.at[index, 'HasAdd'] == "X":
            added += 1
            print("Adicionado:", row['Nome'])

        if added >= limit:
            break

    with pd.ExcelWriter("Networking Escola da Nuvem.xlsx", "xlsxwriter", mode="w") as writer:
        links.to_excel(writer, index=False)
    
    driver.quit()

main()