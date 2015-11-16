from cookiecutter.main import cookiecutter

from getpass import getpass
import os
import sys
from shutil import rmtree

current_path = os.path.abspath('.')
sys.path.append(current_path)

import github, google, mandrill  # NOQA

# opbeat, mandrill, google

# Ensure we have all of the environment variables that we need.
credentials = {
    'github_token': os.getenv('GITHUB_TOKEN') or raw_input('Please enter your Github token (https://github.com/settings/tokens/new, only "repo" is required.): '),

    'mandrill_email': os.getenv('MANDRILL_EMAIL') or raw_input('Please enter your Mandrill email: '),
    'mandrill_password': os.getenv('MANDRILL_PASSWORD') or getpass('Please enter your Mandrill password: '),

    'google_email': os.getenv('GOOGLE_EMAIL') or raw_input('Please enter your Google email: '),
    'google_password': os.getenv('GOOGLE_PASSWORD') or getpass('Please enter your Google password: '),
}

# Call each of the plugins to get the API keys we need.
# credentials.update(
#     github.Plugin().call(credentials)
# )

# opbeat.Plugin.call(credentials)

# credentials.update(
#     mandrill.Plugin().call(credentials)
# )

print google.Plugin().call(credentials)

print credentials

# Remove the directory we created.
rmtree(current_path)


# Generate the project, passing in the API keys we've just obtained.
# cookiecutter('gh:onespacemedia/project-template', extra_context={
#     'foo': 'bar'
# })