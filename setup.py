# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Mcgyver Maze',
    version='0.1.0',
    description='A maze game made with Pygame',
    long_description=readme,
    author='Quentin Lathière',
    url='https://github.com/Synkied/OC_Projet-3',
    license=license,
    packages=find_packages(exclude=('__pycache__', 'resources'))
)
