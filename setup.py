from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme_file:
    readme = readme_file.read()

requirements = ['aiohttp>=3.7.0', 'pydantic>=1.8.0']

setup(
    name="LavaBusiness",
    version="2.0.0",
    description="Async client for lava.ru business-API",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/lztrox/LavaBusiness",
    author="lztrox",
    python_requires='>=3.7',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Framework :: AsyncIO",
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    project_urls={
        "Docs": "https://lavabusiness.readthedocs.io/ru/latest/",
        "Source code": "https://github.com/lztrox/LavaBusiness",
        "Author": "https://github.com/lztrox",
    },
)