from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = '-e .'

def get_requirements(file_path:str) -> List[str]:
    requirements=[]
    with open(file_path) as file_object:
        requirements=file_object.readlines()
        [req.replace('/n','') for req in requirements]

    if (HYPEN_E_DOT in requirements): requirements.remove(HYPEN_E_DOT)
    return requirements

setup( 
    name='ml-deployed',
    version='1.0',
    author='vaishak',
    author_email='vaishakmurali@yahoo.com',
    packages=find_packages(),
    requires=get_requirements('requirements.txt')
)

