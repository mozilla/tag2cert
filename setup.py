from distutils.command.build import build
from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def run(self):
        self.run_command('build')
        _install.run(self)


setup(name="tag2cert",
      version="0.0.1",
      author="Andrew Krugr",
      author_email="akrug@mozilla.com",
      packages=["tag2cert"],
      package_data={},
      license="MPL",
      description="Wrapper for generating certificates during CloudInit \
      using Route53, Let's Encrypt, and Lego.",
      scripts=['bin/tag2cert'],
      url='https://github.com/mozilla/tag2cert',

      download_url="https://github.com/mozilla/tag2cert/archive/v0.0.1.tar.gz",


      use_2to3=True,
      install_requires=[
                        'datetime',
                        'boto3',
                        'logging'
                        ],
      tests_require=[],
      )
