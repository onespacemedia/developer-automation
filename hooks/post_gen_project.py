from cookiecutter.main import cookiecutter

from getpass import getpass
import os
from pprint import pprint
import sys
from shutil import rmtree

current_path = os.path.abspath('.')
sys.path.append(current_path)

import github  # NOQA
import google  # NOQA
import mandrill  # NOQA
import opbeat  # NOQA

# opbeat, mandrill, google

# Ensure we have all of the environment variables that we need.
credentials = {
    'github_token': os.getenv('GITHUB_TOKEN'),
    'github_username': os.getenv('GITHUB_USERNAME') or raw_input('Please enter your Github username: '),
    'github_password': os.getenv('GITHUB_PASSWORD') or getpass('Please enter your Github password: '),

    'mandrill_email': os.getenv('MANDRILL_EMAIL') or raw_input('Please enter your Mandrill email: '),
    'mandrill_password': os.getenv('MANDRILL_PASSWORD') or getpass('Please enter your Mandrill password: '),

    'google_email': os.getenv('GOOGLE_EMAIL') or raw_input('Please enter your Google email: '),
    'google_password': os.getenv('GOOGLE_PASSWORD') or getpass('Please enter your Google password: '),

    'slack_email': os.getenv('SLACK_EMAIL') or raw_input('Please enter your Slack email: '),
    'slack_password': os.getenv('SLACK_PASSWORD') or getpass('Please enter your Slack password: '),
}

# Call each of the plugins to get the API keys we need.
# credentials.update(
#     github.Plugin().call(credentials)
# )

# credentials.update(
#     mandrill.Plugin().call(credentials)
# )

# credentials.update(
#     google.Plugin().call(credentials)
# )

# credentials.update(
#     opbeat.Plugin().call(credentials)
# )

# This is a bit weird, but it's the only way to get the data entered into _this_
# project into the other one.
credentials['project_name'] = "{{ cookiecutter.project_name }}"
credentials['domain_name'] = "{{ cookiecutter.domain_name }}"
credentials['staging_subdomain'] = "{{ cookiecutter.staging_subdomain }}"
credentials['github_name'] = "{{ cookiecutter.github_name }}"
credentials['repo_name'] = "{{ cookiecutter.base_repo_name }}"

credentials['clone_url'] = "git@github.com:onespacemedia/example-project.git"
credentials['email_password'] = 'mandrill_password'
credentials['google_plus_key'] = 'google_plus_key'
credentials['google_plus_secret'] = 'google_plus_secret'
credentials['opbeat_app_id'] = 'opbeat_app_id'
credentials['opbeat_secret_token'] = 'opbeat_secret_token'

pprint(credentials)

print current_path
print current_path.replace('{{ cookiecutter.repo_name }}', '')

# Generate the project, passing in the API keys we've just obtained.
cookiecutter(
    # 'gh:onespacemedia/project-template',
    '~/Workspace/project-template/',
    output_dir=current_path.replace('{{ cookiecutter.repo_name }}', '{{ cookiecutter.base_repo_name }}'),
    extra_context=credentials
)
