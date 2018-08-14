import socket
#import random
#import string
import argparse
import sys

#def main():
	#ip = '192.168.1.254'
	#port = 80
	#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
	#sock.connect((ip, port))
	#request = 'GET /DCIM/MOVIE HTTP/1.1\r\nHost: 192.168.1.254\r\n'
	#request += 'User-Agent: Mozilla/5.0\r\n'
	#request += 'Accept: text/html\r\n\r\n'
	#sock.send(request)
	#data = sock.recv(1024)
	#data = data.split('Content-length: ')[1].split('\r\n')[0]
	#data =  sock.recv(int(data))
	#
	#print 'got data: ', data
	#data = data.split('<a href="')
	#files = []
	#for d in data:
	#	d = d.split('"><b>')
	#	for line in d:
	#		if line.find('.MP4') > 0 and line.find('DCIM') > 0:
	#			if line.find('</a>') < 0:
	#				files.append(line)	
	#
	#for f in files:
	#	print 'file on devcice:' , f
	#
	#delete first file
	#fn  = files[0].split('/DCIM/MOVIE/')[1]
	#print fn
	#
	#request = 'GET /DCIM/MOVIE/%s?del=1 HTTP/1.1\r\nHost: 192.168.1.254\r\n' % (fn)
	#request += 'User-Agent: Mozilla/5.0\r\n'
	#request += 'Accept: text/html\r\n\r\n'
	#print 'request: "'+request+'"'
	#fd = open('never.mp4')
	#post_data = fd.read()
	#fd.close()
	#boundary = '---------------------' 
	#boundary += ''.join(random.choice(string.digits) for _ in range(30))
	#last part first to get the content-length
	#request2 = '-----------------------------240282657716675308522096562468\r\n'
	#request2 += 'Content-Disposition: form-data; name="fileupload1"; filename="Aever.mp4"\r\n'
	#request2 += 'Content-Type: video/mp4\r\n\r\n'
	#request2 += post_data
	#request2 += '\r\n'
	#request2 += '-----------------------------240282657716675308522096562468\r\n'
	#request2 += 'Content-Disposition: form-data; name="upbtn"\r\n'
	#request2 += '\r\n'
	#request2 += 'Upload files\r\n'
	#request2 += '-----------------------------240282657716675308522096562468--\r\n'
	#
	#
	#
	#request =  'POST /DCIM/MOVIE HTTP/1.1\r\n'
	#request += 'Host: 192.168.1.254\r\n'
	#request += 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0\r\n'
	#request += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n'
	#request += 'Accept-Language: en-US,en;q=0.5\r\n'
	#request += 'Accept-Encoding: gzip, deflate\r\n'
	#request += 'Referer: http://192.168.1.254/DCIM/MOVIE\r\n'
	#request += 'Connection: keep-alive\r\n'
	#request += 'Content-Type: multipart/form-data; boundary=---------------------------240282657716675308522096562468\r\n'
	#request += 'Content-Length: %s\r\n\r\n' % (str(len(request2)))
	#request += request2
	#
	#print 'sending file'
	#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
	#sock.connect((ip, port))
	#sock.send(request)
	#print 'sent'
	#print sock.recv(1024)


def connect():
	ip = '192.168.1.254'
	port = 80
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
	sock.connect((ip, port))
	return sock


def get_remote_dir(rpath):
	sock = connect()
	request = 'GET %s HTTP/1.1\r\nHost: 192.168.1.254\r\n' % (rpath)
	request += 'User-Agent: Mozilla/5.0\r\n'
	request += 'Accept: text/html\r\n\r\n'
	sock.send(request)

	data = sock.recv(1024)
	data = data.split('Content-length: ')[1].split('\r\n')[0]
	data = sock.recv(int(data))
	sock.close()
	
	#print 'got data: ', data
	data = ''.join(data).split('<a href="')
	files = []
	for d in data:
		d = d.split('"><b>')
		for line in d:
			if line.find('DCIM') > -1 and line.find('.') > -1:
				if line.find('</a>') < 0:
					files.append(line)	
	
	for f in files:
		print 'file on devcice:' , f
	return	



def list_files(ftype):
	rpath = ''
	if ftype.lower() == 'movie':
		rpath = '/DCIM/MOVIE'
		get_remote_dir(rpath)
	elif ftype.lower() == 'voice':
		rpath = '/DCIM/100VOICE'
		get_remote_dir(rpath)
	elif ftype.lower() == 'pic':
		rpath = '/DCIM/PHOTO'
		get_remote_dir(rpath)
	elif ftype.lower() == 'all':
		rpath = '/DCIM/MOVIE'
		get_remote_dir(rpath)
		rpath = '/DCIM/100VOICE'
		get_remote_dir(rpath)
		rpath = '/DCIM/PHOTO'	
		get_remote_dir(rpath)
		return
	else:
		print 'use the option (movie, voice, pic, all)'
		return


def delete_file(rpath):
	sock = connect()
	request  = 'GET %s?del=1 HTTP/1.1\r\nHost: 192.168.1.254\r\n' % (rpath)
	request += 'User-Agent: Mozilla/5.0\r\n'
	request += 'Accept: text/html\r\n\r\n'
	#print 'request:\n"'+request+'"'
	sock.send(request)
	data = sock.recv(1024)
	#print data
	if data.find('97') > -1:
		print 'file deleted'
	else:
		print 'file already deleted or error'
	sock.close()
	return	


def upload_file(remote_filename, post_path, post_data, content_type):
	request2 = '-----------------------------240282657716675308522096562468\r\n'
	request2 += 'Content-Disposition: form-data; name="fileupload1"; filename="%s"\r\n' % (remote_filename)
	request2 += 'Content-Type: %s\r\n\r\n' % (content_type)
	request2 += post_data
	request2 += '\r\n'
	request2 += '-----------------------------240282657716675308522096562468\r\n'
	request2 += 'Content-Disposition: form-data; name="upbtn"\r\n'
	request2 += '\r\n'
	request2 += 'Upload files\r\n'
	request2 += '-----------------------------240282657716675308522096562468--\r\n'

	request =  'POST %s HTTP/1.1\r\n' % (post_path)
	request += 'Host: 192.168.1.254\r\n'
	request += 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0\r\n'
	request += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n'
	request += 'Accept-Language: en-US,en;q=0.5\r\n'
	request += 'Accept-Encoding: gzip, deflate\r\n'
	request += 'Referer: http://192.168.1.254/DCIM/MOVIE\r\n'
	request += 'Connection: keep-alive\r\n'
	request += 'Content-Type: multipart/form-data; boundary=---------------------------240282657716675308522096562468\r\n'
	request += 'Content-Length: %s\r\n\r\n' % (str(len(request2)))
	request += request2

	print 'sending file'
	sock = connect()
	sock.send(request)
	#print 'sent'
	data =  sock.recv(1024)
	sock.close()
	if data.find('97') > -1:
		print 'file upload success'
	else:
		print 'oh noes! file upload error'
	return

def open_read(file_name):
	fd = open(file_name, 'rb')
	data = fd.read()
	fd.close()
	return data

def open_write(file_name, contents):
	fd = open(file_name, 'wb')
	fd.write(contents)
	fd.close()
	return

def replace_file(blob):
	files = blob.split(':')
	if len(files) != 2:
		print 'files need to be in the format local_file:remote_file'
		return
	#print 'lfile:', files[0], '\nrfile:', files[1]
	rfilename = files[1].split('/')[-1]
	#print rfilename
	rpath = files[1].replace(rfilename, '').rstrip('/')
	#print rpath
	print 'deleting file if exists'
	delete_file(files[1])

	content_type = ''
	if rfilename.lower().find('.mov') > -1:
		content_type = 'video/mp4'
	elif rfilename.lower().find('.wav') > -1:
		content_type = 'audio/wav'
	elif rfilename.lower().find('.jpg') > -1:
		content_type = 'image/jpeg'
	else:
		content_type = 'text/html'
	data = open_read(files[0])
	upload_file(rfilename, rpath, data, content_type)
	return 
	

def grab_files(rpath):
	print 'requesting file'
	sock = connect()
	request = 'GET %s HTTP/1.1\r\nHost: 192.168.1.254\r\n' % (rpath)
	request += 'User-Agent: Mozilla/5.0\r\n'
	request += 'Accept: text/html\r\n\r\n'
	sock.send(request)
	data = sock.recv(1024)
	#print data
	clen = data.split('Content-length: ')[1].split('\r\n')[0]
	print 'content length:', clen
	data = ''
	while int(clen) > len(data):
		part = sock.recv(4096)
		data += part
		print clen, len(data)
	sock.close()
	rpath = rpath.replace('/', '_')
	print 'writing file'
	open_write(rpath, data)
	print 'done'
	return

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-l', '--list', action='store', help='list media on device (movie, voice, pic, all)')
	parser.add_argument('-d', '--delete', action='store', help='delete media from device (filename)')
	parser.add_argument('-r', '--replace', action='store', help='replace media on device (local_filename:remote_filename)')
	parser.add_argument('-g', '--grab', action='store', help='grab media from device (remote_filename)')
	args = parser.parse_args()
	
	if len(sys.argv) < 2:
		parser.print_help()
		sys.exit()
	
	if args.list:
		list_files(args.list)
	if args.delete:
		delete_file(args.delete)
	if args.replace:
		replace_file(args.replace)
	if args.grab:
		grab_files(args.grab)
	#main()
