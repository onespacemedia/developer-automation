from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

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

            try:
                # Open the modal.
                driver.implicitly_wait(5)
                driver.find_element_by_id('projects-create').click()
            except:
                # For some reason, the landing page that is displayed upon logging
                # in to the developer console isn't always the same, so this except
                # block will try alternative routes to get the modal opened.
                driver.find_element_by_xpath('//span[normalize-space(.)="Select a project"]').click()
                driver.find_element_by_xpath('//span[normalize-space(.)="Create a project..."]').click()

            driver.implicitly_wait(30)

            # Fill in the fields.
            driver.find_element_by_id('p6n-project-name-text').send_keys("{{ cookiecutter.project_name }}")
            driver.find_element_by_partial_link_text("Show advanced options").click()

            # Set the storage location.
            driver.find_element_by_id("storageLocation").click()

            driver.find_element_by_css_selector("#storageLocation > div:nth-child(2)").click()
            driver.find_element_by_css_selector("#storageLocation > div:nth-child(2)").send_keys(Keys.UP)
            driver.find_element_by_css_selector("#storageLocation > div:nth-child(2)").send_keys(Keys.UP)
            driver.find_element_by_css_selector("#storageLocation > div:nth-child(2)").send_keys(Keys.RETURN)

            # Sometimes we need to accept the ToS.
            try:
                driver.implicitly_wait(2)
                driver.find_element_by_id('tos-agree').click()
            except:
                pass

            driver.implicitly_wait(30)
            driver.find_element_by_name("ok").click()

            # Switch to the Google+ API screen.
            driver.find_element_by_partial_link_text("Enable and manage APIs")

            if '?project' not in driver.current_url:
                # For some reason, the developer console doesn't always redirect
                # to the new application, this handles that situation.
                print 'No ?project in URL.'
                return {}

            driver.get(driver.current_url.replace('home/dashboard', 'apis/api/plus/overview'))

            # Enable the API.
            driver.find_element_by_css_selector(".p6n-loading-button").click()

            # Go to the consent screen form.
            driver.get(driver.current_url.replace('api/plus/overview', 'credentials/consent'))

            driver.find_element_by_id('p6n-consent-product-name').send_keys("{{ cookiecutter.project_name }}")

            # For some reason clicking this element doesn't always seem to
            # "go through", so we have to be a little.. forceful.
            try:
                while driver.find_element_by_xpath('//span[text()="Save"]'):
                    driver.find_element_by_id('api-consent-save').click()
                    sleep(1)
            except:
                pass

            # Go to the oAuth screen.
            # From: https://console.developers.google.com/apis/credentials?project=single-arcadia-113213&authuser=0
            # To: https://console.developers.google.com/apis/credentials/oauthclient?project=single-arcadia-113213&authuser=0
            driver.find_element_by_css_selector('.p6n-api-credential-dropdown')
            driver.get(driver.current_url.replace('credentials?', 'credentials/oauthclient?'))

            # Configure the client ID.
            driver.find_element_by_css_selector('label.p6n-radio > span.p6n-form-label > span').click()
            driver.find_element_by_xpath("//div[@class='p6n-form-row-input']/input").clear()
            driver.find_element_by_xpath("//div[@class='p6n-form-row-input']/input").send_keys("{{ cookiecutter.project_name }}")
            driver.find_element_by_xpath("//div[@class='p6n-form-row-input']/input").send_keys(Keys.TAB)

            # Enter the Authorized JavaScript origins.
            domains = [
                '127.0.0.1:3000',
                '127.0.0.1:8000',
                'localhost:3000',
                'localhost:8000',
                '{{ cookiecutter.staging_subdomain }}.onespace.media',
                'www.{{ cookiecutter.staging_subdomain }}.onespace.media',
                '{{ cookiecutter.domain_name }}',
                'www.{{ cookiecutter.domain_name }}',
            ]

            for address in domains:
                ActionChains(driver).send_keys('http://{}'.format(address)).send_keys(Keys.RETURN).perform()

            ActionChains(driver).send_keys(Keys.TAB).perform()

            # Enter the callback URLs.
            for address in domains:
                ActionChains(driver).send_keys('http://{}/oauth2callback'.format(address)).send_keys(Keys.RETURN).perform()

            driver.find_element_by_class_name('p6n-loading-button').click()

            # Get the keys from the modal.
            code_elements = driver.find_elements_by_tag_name('code')

            driver.close()

            return {
                'google_plus_key': code_elements[0].text,
                'google_plus_secret': code_elements[1].text,
            }

        except Exception as e:
            print e
            driver.close()
