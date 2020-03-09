from distutils.core import setup

setup(name='WordFinder',
      version='0.1',
      description='CLI tool for finding potential words in a 2D array of letters',
      author='Janet Gainer-Dewar',
      author_email='janet.dewar@gmail.com',
      url='https://github.com/jgainerdewar/word-finder',
      packages=['wordfinder'],
      entry_points={
          'console_scripts': [
              'wordfinder = wordfinder.__main__:main'
          ]
      },
     )