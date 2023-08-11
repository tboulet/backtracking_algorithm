from setuptools import setup, find_namespace_packages

setup(
    name="backtracking",
    url="https://github.com/tboulet/backtracking_algorithm", 
    author="tboulet",
    author_email="timothe.boulet0@gmail.com",
    
    packages=find_namespace_packages(),

    version="0.1.1",
    license="MIT",
    description="A framework for backtracking algorithm, as an interface and a solving function.",
    long_description=open('README.md').read(),     
    long_description_content_type="text/markdown", 
)