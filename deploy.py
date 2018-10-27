#!/usr/bin/python
from shutil import rmtree
import os
import stat
import signal
import subprocess
from shutil import rmtree
from shutil import copyfile
from shutil import copytree
from os.path import expanduser

project = "python-http-server"
install_location = expanduser("~") + "/deployments/" + project

# kill running process
pid_file_location = install_location + "/PID"
if os.path.isfile(pid_file_location):
	with open(pid_file_location, "r") as pid_file:
		pid = pid_file.read()
		print("killing process: " + pid)
		try:
			os.kill(int(pid), signal.SIGTERM)
		except OSError as e:
			print(e)

# remove old installation
if os.path.isdir(install_location):
	rmtree(install_location)

# run application
os.makedirs(install_location)
copytree("public", install_location + "/public")
application_binary = install_location + "/app.py"
copyfile("app.py", application_binary)
permissions = stat.S_IRUSR|stat.S_IWUSR|stat.S_IXUSR
os.chmod(application_binary, permissions)
proc = subprocess.Popen(application_binary)
with open(pid_file_location, "w") as pid_file:
	pid_file.write(str(proc.pid))
print("new application started: " + str(proc.pid))
