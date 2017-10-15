from distutils.core import setup

setup(
    name='curr',
    version='1.1',
    url='',
    license='GPLv3',
    author='granitosaurus',
    author_email='bernardas.alisauskas@protonmail.com',
    description='',
    install_requires=['toml', 'click', 'logzero'],
    py_modules=['curr'],
    entry_points={'console_scripts': ['curr = curr:cli']},

)
