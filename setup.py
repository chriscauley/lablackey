from distutils.core import setup
setup(
  name = 'lablackey',
  packages = {'lablackey':['*']}, # this must be the same as the name above
  version = '0.1.1',
  description = 'A collection of tools for django',
  author = 'Chris Cauley',
  author_email = 'chris@lablackey.com',
  url = 'https://github.com/chriscauley/lablackey', # use the URL to the github repo
  download_url = 'https://github.com/chriscauley/lablackey/tarball/0.1.1', # I'll explain this in a second
  keywords = ['utils'], # arbitrary keywords
  classifiers = [],
)
