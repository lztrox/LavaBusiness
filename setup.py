from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ['httpx>=0.23.1']

setup(
    name="LavaBusiness",
    description="Async client for lava.ru business-API",
    author="lztrox",
    url="https://github.com/lztrox/LavaBusiness",
    version="1.0.0",
    license="Mozilla Public License 2.0 (MPL 2.0)",
    python_requires='>=3.7',
    packages=find_packages(),
    install_requires=requirements,
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Framework :: AsyncIO",
    ],
    project_urls={
        "Docs": "https://lavabusiness.readthedocs.io/ru/latest/",
        "Source code": "https://github.com/lztrox/LavaBusiness",
        "Author": "https://hazedev.ru",
    },
)