import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="fastapi-mongo-restify",
    version="0.0.1",
    description="Rest API configured with pydantic, backed by file database or mongo",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/syntithenai/fastapi-mongo-restify",
    author="Steve Ryan",
    author_email="syntithenai@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["fastapi-mongo-restify"],
    include_package_data=True,
    install_requires=["motor","PyJWT","bcrypt","uvicorn","pymongo","python-decouple","fastapi","pydantic[email]","passlib","motor"],
    
)
