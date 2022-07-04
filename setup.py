from setuptools import setup, find_packages

setup(
    name="tweets_demo",
    version="0.0.1",
    description="tweets_demo",
    author="Team",
    author_email="",
    package_dir={"": "src/"},
    packages=find_packages("src/"),
)

