from setuptools import setup 
  
setup( 
    name='stat386_nba_package', 
    version='0.1', 
    description='Python package for Stat386 project on NBA regular and postseason player performance', 
    author='Sam Wise/Matthew Ng', 
    author_email='samthemanwise@gmail.com', 
    packages=['stat386_nba_package'], 
    install_requires=[ 
        'numpy', 
        'pandas',
        'scikit-learn',
        'matplotlib',
        'seaborn',
        'stats',
        'statsmodels.api'
    ], 
) 