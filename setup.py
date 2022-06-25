from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'pytabular',         # How you named your package folder (MyLib)
  packages = ['pytabular'],   # Chose the same as "name"
  version = '0.1.1',      # Start with a small number and increase it with every change you make
  license='MIT',
  description = 'Connect to your tabular model and perform operations programmatically',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Curtis Stallings',
  author_email = 'curtisrstallings@gmail.com',
  url = 'https://www.linkedin.com/in/curtisrs/',
  download_url = '', 
  keywords = ['tabular','PowerBI','AAS','DAX'],
  install_requires=[
          'pythonnet','pandas','InquirerPy'
      ],
  classifiers=[
    'Development Status :: 3 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Database',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python :: 3.10'
  ],
)