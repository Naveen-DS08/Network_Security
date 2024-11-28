from setuptools import find_packages, setup 
from typing import List 

def get_requirements()->List[str]:
    """
    This function will return list of requirements
    """
    list_of_requirements:List[str] = []
    try:
        with open("requirements.txt", "r") as file:
            # Read lines from file 
            lines = file.readlines()
            for line in lines:
                requirements = line.strip()
                # ignore empty lines and -e . 
                if requirements and requirements != "-e .":
                    list_of_requirements.append(requirements)
    except FileNotFoundError:
        print("requirements.txt file not found!")

    return list_of_requirements

setup(
    name= "Network Security",
    version = "0.0.1",
    author="Naveen Babu",
    author_email="naveenmails814@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements()
)