from setuptools import setup, find_packages
from sys import version_info, exit, stderr

with open("PyPi-README.rst") as f:
    long_description = f.read().replace("\r", "")

if version_info < (2, 7, 0) or (version_info[0] == 3 and version_info < (3, 2, 0)):
    stderr.write('zIRC requires Python 2.7 or 3.2 and higher')
    exit(-1)

setup(name='zirc',
      version='0.1.0',
      description='A Python client to interact with powdertoy.co.uk',
      long_description=long_description,
      url='https://github.com/wolfy1339/tptapi',
      author='wolfy1339',
      author_email='webmaster@wolfy1339.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['six', 'requests'],
      include_package_data=True,
      zip_safe=False,
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
      ])
