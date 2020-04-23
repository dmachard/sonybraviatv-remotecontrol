#!/usr/bin/python

import setuptools
from sonybraviatv_remotecontrol import __version__

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()
    
KEYWORDS = ('sony bravia tv simple ip remote control')

setuptools.setup(
    name="sonybraviatv_remotecontrol",
    version=__version__,
    author="Denis MACHARD",
    author_email="d.machard@gmail.com",
    description="Python remote control gateway for sony bravia tv",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/dmachard/sonybraviatv_remotecontrol",
    packages=['sonybraviatv_remotecontrol'],
    include_package_data=True,
    platforms='any',
    keywords=KEYWORDS,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ],
    entry_points={'console_scripts': ['sonybraviatv_remotecontrol = sonybraviatv_remotecontrol.gateway:start_remotecontrol']},
    install_requires=[
        "websockets"
    ]
)
