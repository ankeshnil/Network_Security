'''
find_packages it scann all folder and where it fine __init__.py file
it consider it as a package

setup.py file work is to set up the project as a python package
in requirements.txt there is -e . . when we execute requirements.txt , -e . refer this setup.py file
to execute this file also
'''


from setuptools import find_packages, setup  
from typing import List

hypen_e_dot = '-e .'
def get_requirements()->List[str]:
    '''
    This function we return the list of all the requirements
    '''
    requirments_list:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            # real the file line by lile
            liens = file.readlines()
            # process each line 
            for line in liens:
                # ignore the /n or space
                requirments = line.strip()
                # ignore the empty line and -e .
                if requirments and requirments != '-e .':
                    requirments_list.append(requirments)
        
    
    except FileExistsError:
        print("file not not found requiremnt.txt")
        
    return requirments_list


setup(
    name = 'Network Security',
    version= '0.0.1',
    author = 'Ankesh',
    author_email = 'ankeshnil00@gmai.com',
    packages = find_packages(),  # if find- src has __init__.py , So src is a package , and src contail all our project code file
    install_requires = get_requirements()
) 