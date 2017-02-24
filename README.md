# ABANDONED

# developer-automation

This is a project used by the developers at [Onespacemedia](http://www.onespacemedia.com) to start new [CMS](/onespacemedia/cms/) projects using our [project template](/onespacemedia/project-template) configured and ready to go.

It makes use of the excellent [Cookiecutter](https://github.com/audreyr/cookiecutter) project to generate the final YML file which is passed into the project template (which also uses Cookiecutter).

## What it configures / gets API keys for:

* Github private repository
* Mandrill API key
* Google+ oAuth credentials
* Opbeat

We have a bunch of Github hooks setup at the organisation level, so we don't need to define those at the repository level.

## Usage

```
cd ~/Workspace
pip install cookiecutter
cookiecutter gh:onespacemedia/developer-automation
```
