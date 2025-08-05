# setup.py
from setuptools import setup, find_packages

setup(
    name='commit_intel',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer[all]",
        "langchain",
        "langgraph",
        "gitpython",
        "xmltodict",
        "tiktoken",
        "openai",      # or "ollama" if you're using that
    ],
    entry_points={
        'console_scripts': [
            'review = cli.review:app',
        ],
    },
    author="Aniket Indulakr",
    description="AI-powered local commit and test coverage reviewer for Android engineers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires='>=3.8',
)
