How do I install the project?
- run the following:
    - cd /path/to/yourproject
    - mkdir -p src/projectfile
    - touch setup.py and paste the code below:
    from setuptools import setup, find_packages
    setup(
        name="yourproject",
        version="0.0.1",
        description="yourproject",
        author="Team",
        author_email="",
        package_dir={"": "src/"},
        packages=find_packages("src/"),
    )

    - pip install virtualenv
    - virtualenv venv
    - source venv/bin/activate
    - pip install -r requirements.txt
    - alembic init alembic
    - pip install -e .
