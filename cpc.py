import os
import sys
import getopt
import shutil

CPC_ROOT = '/Users/linjw/workspace/cpp-project-creator/'
TEMPLATE = os.path.join(CPC_ROOT, 'template')

PWD = os.path.abspath(os.curdir)
VERSION = 'VERSION'
EMAIL = 'BUG-REPORT-ADDRESS'

def DealWithConfigureLine(line, proj, version, email):
    if line.startswith('AC_INIT'):
        line = line.replace('FULL-PACKAGE-NAME', proj)
        line = line.replace('VERSION', version)
        line = line.replace('BUG-REPORT-ADDRESS', email)
        line = [line, 'AM_INIT_AUTOMAKE([-Wall -Werror foreign])\n']
    return line

def ExecCommand(command):
    print(command + '...')
    os.system(command)

def GenConfigureAc(proj, version, email):
    print('gen configure.ac ..')
    ExecCommand('autoscan')
    ac = []
    with open('configure.scan') as configure:
        for line in configure:
            ac.extend(DealWithConfigureLine(line, proj, version, email))
    with open('configure.ac', 'w') as configure:
        configure.writelines(ac)
    os.remove('configure.scan')

def SetProjectName(proj):
    for source in ('src/Makefile.am', 'src/main.cpp', 'examples/example_main.cpp'):
        print('dwal with ' + source + '...')
        lines = []
        with open(source) as file:
            for line in file: lines.append(line.replace('{}', proj))
        with open(source, 'w') as file:
            file.writelines(lines)

def InitProj(path, proj, version, email):
    os.chdir(path)
    SetProjectName(proj)
    GenConfigureAc(proj, version, email)
    ExecCommand('autoreconf --install')

def CpyFilesFromDir(srcDir, dstDir):
    for item in os.listdir(srcDir):
        src = os.path.join(srcDir, item)
        dst = os.path.join(dstDir, item)
        if os.path.isdir(src): shutil.copytree(src, dst)
        else: shutil.copy2(src, dst)

def RecvArgvs(argv):
    proj,version,email= None,None,None
    opts, args = getopt.getopt(argv[1:], 'p:v:e:')
    for op, value in opts:
        if op == "-p": proj = value
        elif op == "-v": version = value
        elif op == "-e": email = value
    return proj or os.path.basename(PWD), version or VERSION, email or EMAIL, proj

def main(argv):
    proj,version,email,dst= RecvArgvs(argv)
    if not dst: CpyFilesFromDir(TEMPLATE, PWD)
    else: shutil.copytree(TEMPLATE, dst)
    InitProj(dst or PWD, proj, version, email)

if __name__ == '__main__':
    main(sys.argv)
