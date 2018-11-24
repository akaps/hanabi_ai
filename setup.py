from distutils.core import setup

setup(name='hanabi_ai',
      version='1.0',
      description='Hanabi AI',
      author='akaps',
      author_email='ari.kaps@gmail.com',
      url='https://github.com/akaps/hanabi_ai',
      packages=['hanabi_ai'],
      scripts=['hanabi_ai/sample.sh',
               'hanabi_ai/sample_tournament.sh'],
     )
