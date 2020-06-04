#####################################################
#               NUITKA BUILD SCRIPT                 #
#####################################################
# Author: Matic Kukovec
# Date: April 2018

import os
from multiprocessing import cpu_count

TARGET = "supervised"
NUITKA = "D:/Anaconda3/Scripts/nuitka3"  # Path where my nuitka3 is
CWD = os.getcwd().replace("\\", "/")
MSVC_VER = "14.1"
MSVC = "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/VC/Auxiliary/Build/vcvars64.bat"
NUMBER_OF_CORES_FOR_COMPILATION = cpu_count() # 1 is the safest choice, but you can try more
OUTPUT_DIR = "{}".format(CWD)
# # clear old build
# os.system("rm -rf %s.exe"%TARGET)
# os.system("rm -rf %s.dist"%TARGET)
# os.system("rm -rf %s.build"%TARGET)
# build命令
command = '"{}" amd64 & '.format(MSVC)
command += "{} ".format(NUITKA)
command += " --msvc={}".format(MSVC_VER)
command += " --output-dir={} ".format(OUTPUT_DIR)
# command += " --verbose "
command += " --jobs={} ".format(NUMBER_OF_CORES_FOR_COMPILATION)
command += " --show-scons"
command += " --remove-output"
command += " --windows-disable-console"
# command += " --icon={}/myicon.ico ".format(CWD)
command += " --standalone "
# command += " --run "
command += " {}/{}.py ".format(CWD,TARGET)

print(command)
os.system(command)
print("BUILD-FINISHED")