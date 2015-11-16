import github3


class Plugin:

    def two_factor_callback(self):
        code = ''
        while not code:
            # The user could accidentally press Enter before being ready,
            # let's protect them from doing that.
            code = raw_input('Enter 2FA code: ')
        return code

    def call(self, credentials):
        g = github3.login(
            token=credentials['github_token']
        )

        repo = g.organization('onespacemedia').create_repo(**{
            'name': '{{ cookiecutter.github_name }}',
            'description': '{{ cookiecutter.project_name }}',
            {% if cookiecutter.domain_name %}'homepage': 'http://{{ cookiecutter.domain_name }}',{% endif %}
            'private': True,
            'has_wiki': False,
            'has_downloads': False,
        })

        return {
            'clone_url': repo.clone_url
        }
