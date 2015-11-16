from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from time import sleep


class Plugin:

    def call(self, credentials):
        # ------------------------------------------------------------------------ #
        #                          GOOGLE PLUS APPLICATION                         #
        # ------------------------------------------------------------------------ #

        # XXX: Unfortunately the Google Developers Console is an AngularJS
        #      application so it's a little harder to navigate compared to a regular
        #      webpage. This makes all of this code a little awkward.

        """
        https://console.developers.google.com/home/dashboard?project=example-project-2-1131&authuser=0
        https://console.developers.google.com/apis/api/plus/overview?project=example-project-2-1131&authuser=0
        https://console.developers.google.com/apis/credentials/consent?project=example-project-2-1131&authuser=0
        https://console.developers.google.com/apis/credentials/oauthclient?project=example-project-2-1131&authuser=0
        """
        driver = webdriver.Firefox()
        driver.implicitly_wait(30)

        try:
            driver.get('https://console.developers.google.com/project')

            # Log in to the developer console.
            driver.find_element_by_id('Email').send_keys(credentials['google_email'])
            driver.find_element_by_id('next').click()

            driver.find_element_by_id('Passwd').send_keys(credentials['google_password'])
            driver.find_element_by_id('signIn').click()

            # Create the initial project.

            # Open the modal.
            driver.find_element_by_id('projects-create').click()

            # Fill in the fields.
            driver.find_element_by_id('p6n-project-name-text').send_keys("{{ cookiecutter.project_name }}")
            driver.find_element_by_partial_link_text("Show advanced options").click()

            # Set the storage location.
            driver.find_element_by_id("storageLocation").click()

            driver.find_element_by_css_selector("#storageLocation > div:nth-child(2)").click()
            driver.find_element_by_css_selector("#storageLocation > div:nth-child(2)").send_keys(Keys.UP)
            driver.find_element_by_css_selector("#storageLocation > div:nth-child(2)").send_keys(Keys.RETURN)

            driver.find_element_by_name("ok").click()

            # Switch to the Google+ API screen.
            driver.find_element_by_partial_link_text("Enable and manage APIs")
            driver.get(driver.current_url.replace('home/dashboard', 'apis/api/plus/overview'))

            # Enable the API.
            driver.find_element_by_css_selector(".p6n-loading-button").click()

            # Go to the consent screen form.
            driver.get(driver.current_url.replace('api/plus/overview', 'credentials/consent'))

            driver.find_element_by_id('p6n-consent-product-name').send_keys("{{ cookiecutter.project_name }}")
            driver.find_element_by_id('api-consent-save').click()

            # Go to the credentials screen.
            driver.find_element_by_css_selector(".jfk-button-primary")
            driver.get(driver.current_url.replace('credentials', 'credentials/consent'))

            # Configure the client ID.
            driver.find_element_by_css_selector('label.p6n-radio > span.p6n-form-label > span').click()
            driver.find_element_by_xpath("//div[@class='p6n-form-row-input']/input").send_keys("{{ cookiecutter.project_name }}")

            # Enter the Authorized JavaScript origins.
            return {}

            """
            # Go to the API list and enable the Google+ API.
            elem = WebDriverWait(driver, 45).until(
                EC.presence_of_element_located((By.ID, '126_jsmod_apiui_api'))
            )
            elem.click()

            elem = WebDriverWait(driver, 45).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.p6n-api-search input'))
            )
            elem.send_keys('Google+ API')

            sleep(3)

            elem = WebDriverWait(driver, 45).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'table.p6n-table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(1) > a'))
            )
            elem.click()

            # Enable API
            elem = WebDriverWait(driver, 45).until(
                EC.visibility_of_element_located((By.XPATH, '//jfk-button/span[text()="Enable API"]'))
            )
            elem.click()

            # Wait for disable button to appear
            elem = WebDriverWait(driver, 45).until(
                EC.visibility_of_element_located((By.XPATH, '//jfk-button/span[text()="Disable API"]'))
            )

            # Go to the credentials page.
            driver.find_element_by_id('126_jsmod_apiui_credential').click()

            elem = WebDriverWait(driver, 45).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Create new Client ID")]'))
            )
            elem.click()

            elem = WebDriverWait(driver, 45).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea.ng-valid-origin-path'))
            )
            elem.clear()
            elem.send_keys("http://127.0.0.1:8000")

            elem = WebDriverWait(driver, 45).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.modal-dialog-buttons button:first-of-type'))
            )
            elem.click()

            elem = WebDriverWait(driver, 45).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.p6n-kv-list-item:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(1)'))
            )
            google_plus_client_id = elem.text

            elem = WebDriverWait(driver, 45).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.p6n-kv-list-item:nth-child(3) > div:nth-child(2) > div:nth-child(1) > span:nth-child(1)'))
            )
            google_plus_client_secret = elem.text

            driver.close()

            return {
                'google_plus_client_id': google_plus_client_id,
                'google_plus_client_secret': google_plus_client_secret,
            }
            """
        except Exception as e:
            print e
            driver.close()
