from setuptools import setup

# architecture
pkg=[
    "tobi",
    "tobi.results",
    "tobi.protocol",
    "tobi.system",
    "tobi.utils",
]
# non python data to keep
pkg_data={}

setup(
   name='tomiBIMMS',
   version='0.0.1',
   description='BIMMS python API',
   long_description = 'file: README.md',
   author='Thomas Couppey - Louis Regnacq - Florian Kolbl',
   packages=pkg,
   package_data=pkg_data,
   include_package_data=True,
   url = 'https://github.com/ThomasCouppey/tomoBIMMS.git',
   classifiers =[
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent'
     ],
    install_requires=['numpy','andi-py','matplotlib','scipy', 'bimms', 'pyEIT'], #external packages as dependencies
    python_requires = '>=3.6',
)
