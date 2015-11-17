from selenium import webdriver


class Plugin:

    def two_factor_callback(self):
        code = ''
        while not code:
            # The user could accidentally press Enter before being ready,
            # let's protect them from doing that.
            code = raw_input('Enter 2FA code: ')
        return code

    def call(self, credentials):
        # ------------------------------------------------------------------------ #
        #                                 OPBEAT                                   #
        # ------------------------------------------------------------------------ #

        driver = webdriver.Firefox()
        driver.implicitly_wait(30)

        driver.get('https://opbeat.com/onespacemedia/new-app/')

        driver.find_element_by_partial_link_text("Sign in with GitHub").click()

        driver.find_element_by_id("login_field").send_keys(credentials['github_username'])
        driver.find_element_by_id("password").send_keys(credentials['github_password'])
        driver.find_element_by_name("commit").click()

        # We may have a 2FA on the account, check for this.
        try:
            driver.implicitly_wait(5)
            driver.find_element_by_name('otp').send_keys(self.two_factor_callback())
            driver.find_element_by_css_selector('button.btn').click()
        except Exception:
            pass

        driver.implicitly_wait(30)

        driver.find_element_by_name("name").send_keys("{{ cookiecutter.project_name }}")

        # Set the stack to Django
        driver.find_element_by_xpath("//form[@class='parsley-form']/div[1]/div[2]/div[2]/div/label/span").click()

        # Set the deployment method to Fabric.
        driver.find_element_by_xpath("//form[@class='parsley-form']/div[1]/div[3]/div[2]/div/label[3]/span").click()

        # Submit the form.
        driver.find_element_by_xpath("//div[@class='footer']/input").click()

        # Connect to Github
        driver.find_element_by_partial_link_text("Connect").click()
        driver.find_element_by_css_selector('option[value="onespacemedia/{{ cookiecutter.github_name }}"]').click()
        driver.find_element_by_xpath("//div[@class='repository-day-container']/form/button").click()

        # Connect to Slack
        driver.get(driver.current_url.replace('module-setup/instructions', 'settings/integrations/slack/new'))
        driver.find_element_by_name("alarm").click()

        # Slack currently have some issues with JS on their page, this is a workaround.
        try:
            driver.find_element_by_css_selector('body')
        except:
            pass

        # Enter the Slack subdomain.
        driver.find_element_by_name("domain").send_keys("onespacemedia")
        driver.find_element_by_id("oauth_pick_signin").click()

        # Slack currently have some issues with JS on their page, this is a workaround.
        try:
            driver.find_element_by_css_selector('body')
        except:
            pass

        # Log in to Slack.
        driver.find_element_by_id("email").send_keys(credentials['slack_email'])
        driver.find_element_by_id("password").send_keys(credentials['slack_password'])
        driver.find_element_by_id("signin_btn").click()

        # Slack currently have some issues with JS on their page, this is a workaround.
        try:
            driver.find_element_by_css_selector('body')
        except:
            pass

        # We may have a 2FA on the account, check for this.
        try:
            driver.implicitly_wait(5)
            driver.find_element_by_name('2fa_code').send_keys(self.two_factor_callback())
            driver.find_element_by_id('signin_btn').click()
        except Exception:
            pass

        driver.implicitly_wait(30)

        # Slack currently have some issues with JS on their page, this is a workaround.
        try:
            driver.find_element_by_css_selector('body')
        except:
            pass

        # Select the channel.
        driver.find_element_by_xpath("//div[@class='fsl_value']//div[normalize-space(.)='Select channel']").click()
        driver.find_element_by_xpath("//div[@class='fsl_list']//div[normalize-space(.)='#commits']").click()
        driver.find_element_by_id('oauth_authorizify').click()

        # Disable errors and comments in the commits channel.
        driver.find_element_by_name('name').clear()
        driver.find_element_by_name('name').send_keys('Releases')
        driver.find_element_by_css_selector('[for="id_errorgroup"]').click()
        driver.find_element_by_css_selector('[for="id_comment"]').click()
        driver.find_element_by_name("alarm").click()

        # Add the 2nd Slack integration for the errors channel.
        driver.get(driver.current_url.replace('integrations/', 'integrations/slack/new'))
        driver.find_element_by_name("alarm").click()

        # Slack currently have some issues with JS on their page, this is a workaround.
        try:
            driver.find_element_by_css_selector('body')
        except:
            pass

        # Select the channel.
        driver.find_element_by_xpath("//div[@class='fsl_value']//div[normalize-space(.)='Select channel']").click()
        driver.find_element_by_xpath("//div[@class='fsl_list']//div[normalize-space(.)='#errors']").click()
        driver.find_element_by_id('oauth_authorizify').click()

        # Disable releases in the commits channel.
        driver.find_element_by_name('name').clear()
        driver.find_element_by_name('name').send_keys('Errors')
        driver.find_element_by_css_selector('[for="id_release"]').click()
        driver.find_element_by_name("alarm").click()

        # Finally, get the app ID.
        driver.get(driver.current_url.replace('settings/integrations', 'releases/setup/instructions'))
        tokens = driver.find_elements_by_class_name('token')

        driver.close()

        return {
            'opbeat_organization_id': tokens[0].text,
            'opbeat_app_id': tokens[1].text,
            'opbeat_secret_token': tokens[2].text,
        }
