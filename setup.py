from setuptools import setup

setup(name='scrum-update',
      version='0.1.0',
      description='To send out a daily scrum update for in-progress tasks for all the users of the given project',
      long_description=open('README.md').read(),
      url='https://github.com/samarthg/dailyscrumupdate',
      download_url = 'https://github.com/samarthg/jira-scrum-update-automation/archive/v0.1.0.tar.gz',
      author='Samarth Gahire',
      author_email='samarth.gahire@gmail.com',
      license='MIT',
      packages=['scrum_update'],
      install_requires=[
          'jinja2',
          'jira==1.0.10',
          'bumpversion',
          'fabric3',
      ],
      zip_safe=False,
      entry_points={
          'console_scripts': [
              's3streamcat = scrum_update.scrum_update:'
          ]
      },
      keywords = ['jira', 'scrum', 'standup', 'update'],
      )
