#!/usr/bin/env python

import os
import shutil

TEMPLATE = 'template'
CPC = 'cpc'
BIN_DIR = '/usr/local/bin'
shutil.copytree(TEMPLATE, os.path.join(os.getenv('HOME'), '.cpc', TEMPLATE))
shutil.copy2(CPC, os.path.join(BIN_DIR, CPC))
