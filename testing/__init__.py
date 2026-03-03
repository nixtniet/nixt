# This file is placed in the Public Domain.
# pylint: disable=C0413,R0801
# ruff: noqa: F403,F405


"testing"


import os
import sys


sys.path.insert(0, os.getcwd())


from nixt.booting import db


db.setwd(".test")
