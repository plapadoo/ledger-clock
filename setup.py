from setuptools import setup, find_packages

setup(
    name="ledger-clock",
    version="1.0",
    description="Tool for creating and managing time logs with ledger",
    python_requires='>=3.6.1',
    entry_points={
        'console_scripts': ['ledgerclock = ledgerclock.__main__:main']
    },
    long_description='',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    keywords='ledger',
    url='https://github.com/plapadoo/ledger-clock',
    author='plapadoo',
    author_email='info@plapadoo.de',
    license='BSD3',
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    zip_safe=True)
