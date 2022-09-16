from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver

import selenium.webdriver.support.expected_conditions as EC
import time
import sys


class BotChallenger:
    def __init__(self, accessCode: str, firstName: str, lastName: str, birthDate: str, phoneNumber: str, street: str, city: str, state: str, zip: str, email: str):
        # Unique access code & Registration Email
        self.accessCode = accessCode
        self.email = email

        # Personal details for Registration
        self.firstName = firstName
        self.lastName = lastName
        self.birthDate = birthDate
        self.phoneNumber = phoneNumber

        # Location for Registration
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip

    def start(self):
        # Create Webdriver
        chromeOptions = Options()
        chromeOptions.add_argument("--log-level=3")
        chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"])
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
        chromeOptions.add_experimental_option("useAutomationExtension", False)

        webDriver = webdriver.Chrome(chrome_options=chromeOptions)
        # head over to the challenge's page
        webDriver.get("https://www.eatswendymorty.com")

        # define data to be typed
        element_xpaths = ['//*[@id="access-code"]',
                          '//*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div[1]/input',
                          '//*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[2]/div[2]/input',
                          '//*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[3]/div/div/div/input',
                          '//*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[4]/div/input',
                          '//*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[5]/div/input',
                          '//*[@id="address-start"]',
                          '//*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[8]/div[1]/input',
                          '//*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[8]/div[2]/input',
                          '//*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[8]/div[3]/input']
        element_data = [self.accessCode, self.firstName, self.lastName, self.birthDate, self.phoneNumber, self.email,
                        self.street, self.city, self.state, self.zip]
        # loop between all the typeable elements
        for index, value in enumerate(element_xpaths):
            try:
                # wait until element is visible
                textbox = WebDriverWait(webDriver, 5).until(EC.element_to_be_clickable((By.XPATH, value)))
                if textbox is None:
                    raise Exception("Textbox was never found?")
                # type if visible
                textbox.send_keys(element_data[index])
            except Exception as e:
                sys.exit(e)

        # scroll down, so we can select the TOS button and submit
        webDriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # select the TOS Button
        button = WebDriverWait(webDriver, 5).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[10]/div/label/input')))
        webDriver.execute_script("arguments[0].click();", button)

        # spam the submit button until we see what happens
        while True:
            # if we've won or lost, we can check via here
            if "Congratulations, you've won!" in webDriver.page_source:
                return True
            elif "You didn't win this time" in webDriver.page_source:
                # end the webdriver
                webDriver.close()
                return False
            # otherwise we can just stay in the loop of spamming the button.
            else:
                button = WebDriverWait(webDriver, 10).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="root"]/div/div/div/div/div[2]/div/div[2]/div[11]/div/button')))
                webDriver.execute_script("arguments[0].click();", button)
                time.sleep(1)
