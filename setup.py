#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Setup script for glob
'''
# import os
# _USERNAME = os.getenv("SUDO_USER") or os.getenv("USER")
# _HOME = os.path.expanduser("~"+_USERNAME)
# _CONFIGDIR = os.path.join(_HOME, ".config")

from setuptools import setup

setup(name="glob",
      version="1.0",
      description="",
      long_description="""
      Simple module to ...
      """,
      author="Julien Spronck",
      author_email="github@frenetic.be",
      url="http://frenetic.be",
      packages=["glob"],
#       entry_points = {"console_scripts":["glob = "
#                                          "glob:main"]},
#       data_files=[(_CONFIGDIR, ["glob/glob_config.py"])],
      license="Free for non-commercial use",
     )

