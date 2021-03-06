from distutils.core import setup

setup(name='hanabi_ai',
      version='1.0',
      description='Hanabi AI',
      author='akaps',
      author_email='ari.kaps@gmail.com',
      url='https://github.com/akaps/hanabi_ai',
      packages=['hanabi_ai', 'hanabi_ai.model', 'hanabi_ai.players', 'hanabi_ai.tests'],
      scripts=['sample.sh',
               'sample_tournament.sh'],
     )
