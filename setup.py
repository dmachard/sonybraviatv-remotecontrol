#!/usr/bin/python

import setuptools
from kodi_remotecontrol import __version__

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()
    
KEYWORDS = ('sony bravia tv simple ip remote control')

setuptools.setup(
    name="sonybravia_remotecontrol",
    version=__version__,
    author="Denis MACHARD",
    author_email="d.machard@gmail.com",
    description="Python remote control gateway for sony bravia tv",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/dmachard/sonybravia_remotecontrol",
    packages=['sonybravia_remotecontrol'],
    include_package_data=True,
    platforms='any',
    keywords=KEYWORDS,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ],
    entry_points={'console_scripts': ['sonybravia_remotecontrol = sonybravia_remotecontrol.wsproxy:start_remotecontrol']},
    install_requires=[
        "websockets"
    ]
)
