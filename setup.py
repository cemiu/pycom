import os
from setuptools import setup, find_packages

with open('pycom/version.txt') as f:
    version = f.read().strip()

with open('README.md') as f:
    long_description = f.read()

extras_require = {
    'flask': ['Flask'],
    'flask-caching': ['Flask-Caching'],
    'flask-parameter-validation': ['Flask-Parameter-Validation']
}

setup(
    name='pycom',
    version=version,
    description='Library for interacting with the Pycom database of coevolution matrices of proteins',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/pycom',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'h5py'
    ],
    extras_require=extras_require,
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
