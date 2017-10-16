from setuptools import setup

setup(
    name='curr',
    version='1.12',
    url='https://github.com/Granitosaurus/curr',
    license='GPLv3',
    author='granitosaurus',
    author_email='bernardas.alisauskas@protonmail.com',
    description='currency converter cli app',
    install_requires=['toml', 'click', 'logzero'],
    py_modules=['curr'],
    entry_points={'console_scripts': ['curr = curr:cli']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ]
)
