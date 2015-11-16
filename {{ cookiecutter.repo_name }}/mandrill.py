from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Plugin:

    def call(self, credentials):
        driver = webdriver.Firefox()

        driver.get('https://mandrillapp.com/settings')

        driver.find_element_by_id('username').send_keys(credentials['mandrill_email'])
        driver.find_element_by_id('password').send_keys(credentials['mandrill_password'])
        driver.find_element_by_id('password').send_keys(Keys.RETURN)

        driver.find_element_by_id('show-key-form').click()
        driver.find_element_by_id('key-description').send_keys("{{ cookiecutter.project_name }}")
        driver.find_element_by_id('btn-submit').click()

        elem = driver.find_element_by_xpath('//td[contains(text(), "{{ cookiecutter.project_name }}")]')
        elem = elem.find_element_by_xpath('..')

        driver.close()

        return {
            'mandrill_password': elem.get_attribute('data-key'),
        }
