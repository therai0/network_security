from setuptools import find_packages,setup
from typing import List


requirement_lst:List[str] = []
def get_requirements()->List[str]:
    """
    This function will return the list of the requirements in to form of list[]
    """
    try:
        with open("requirements.txt",'r') as file:
            # read lines from the file
            lines = file.readlines()
            # process each line
            for line in lines:
                # remove the extra space in begning and end
                requirement = line.strip()
                if requirement and requirement != "-e .":
                    requirement_lst.append(requirement)
        return requirement_lst
    except FileNotFoundError:
        print("Requirement.txt file not found")
    


setup(
    name="Network security",
    author="rai_bhaskar",
    version="0.0.1",
    author_email="bhaskar@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)