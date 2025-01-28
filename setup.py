from setuptools import setup, find_packages
from typing import List
import os

if __name__ == "__main__":
    setup()



# def read_requirements(filename: str) -> List[str]:
#     with open(filename) as f:
#         return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# setup(
#     name='Our_Compiler',
#     version='0.1.0',
#     packages=find_packages(where="src"),
#     package_dir={"": "src"},
#     install_requires=read_requirements('requirements.txt'),
#     extras_require={
#         "dev": read_requirements('requirements_dev.txt'),
#     },
#     author='Balgopal Moharana',
#     author_email='moharanabalgopal@iitgn.ac.in',
#     description='Implementation of a compiler for a simple language',
#     long_description=open('README.md').read() if os.path.exists('README.md') else "",
#     long_description_content_type='text/markdown',
#     url='https://github.com/lucifer-reborn473/Our_Compiler',
#     classifiers=[
#         'Programming Language :: Python :: 3',
#         'License :: OSI Approved :: MIT License',
#         'Operating System :: OS Independent',
#     ],
#     python_requires='>=3.10',
# )