from setuptools import setup, find_packages
from sys import version_info, stderr
from sys import exit as _exit
import os

with open("README.rst") as f:
    long_description = f.read().replace("\r", "")

with open("requirements.txt") as r:
    requirements = r.read().replace("\r","").strip().split("\n")

if version_info < (2, 7, 0) or (version_info[0] == 3 and
                                version_info < (3, 3, 0)):
    stderr.write('tptapi requires Python 2.7 or 3.3 and higher')
    _exit(-1)

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, 'tptapi', '__version__.py'), 'r') as f:
    exec(f.read(), about) # pylint: disable=exec-used

setup(name='tptapi',
      version=about["__version__"],
      description=about['__description__'],
      long_description=long_description,
      url=about['__url__'],
      author='wolfy1339',
      author_email='webmaster@wolfy1339.com',
      license=about['__license__'],
      packages=find_packages(),
      python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*'
      install_requires=requirements,
      include_package_data=True,
      zip_safe=False,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Internet :: WWW/HTTP'
      ])
