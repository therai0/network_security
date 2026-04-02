
from gettext import find
from setuptools import find_packages,setup
from typing import List


def get_requirements()->List[str]:
    """
    It will return all the requirements 
    """
    req_list:List[str]= []
    try:
        with open("requirements.txt",'r') as file:
            # read lines from the file
            lines = file.readlines()

            for line in lines:
                # black space and -e. is ignore
                requirement = line.strip()
                if requirement.strip() and requirement.strip() != "-e .":
                    req_list.append(requirement)
                

    except FileNotFoundError:
        print("requirement.txt file is not found")

    return req_list




setup(
    name="Networksecurity",
    version="0.0.1",
    author="Bhaskar Rai",
    author_email="iamraibhaskar@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements()
)