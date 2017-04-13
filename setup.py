#!/usr/bin/env python

import os
import shutil
import sys

TEMPLATE = 'template'
CPC_ROOT = os.path.join(os.getenv('HOME'), '.cpc')

CPC = 'cpc'
BIN_DIR = '/usr/local/bin'
CPC_BIN  = os.path.join(BIN_DIR, CPC)

if len(sys.argv)>1 and sys.argv[1]=='uninstall':
    try:
        if os.path.exists(CPC_ROOT): shutil.rmtree(CPC_ROOT)
        if os.path.exists(CPC_BIN): os.remove(CPC_BIN)
    except Exception,e:
        print(e)
else:
    try:
        shutil.copytree(TEMPLATE, os.path.join(CPC_ROOT, TEMPLATE))
        shutil.copy2(CPC, CPC_BIN)
    except Exception,e:
        print(e)
        print('use argv uninstall to remove ' + CPC_BIN + ' and ' + CPC_ROOT)
