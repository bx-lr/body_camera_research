import struct
import binascii
import sys

def main():
    #// DigitalAlly.Security.Cryptography.LWE
    '''
	private static uint CRYPT(uint data, uint offset)
	{
		return (data ^ 129 + ~(offset * 21 + 1)) & 0xFF;
	}
    '''
    infile = sys.argv[1]
    outfile = sys.argv[2]
    fd = open(infile, 'rb')
    data = fd.readlines()
    fd.close()

    #holds the output string
    tmp = ''    
    for line in data:
        #skip past 0001 0002 etc.
        if len(line) > 10:
            print line

            #figure out if we should decode or encode
            if line.find('SN=') > -1:
                decode = False
                bline = line
            else:
                decode = True
                line = line.rstrip('\r\n')
                bline = binascii.unhexlify(line)

            #acutal encode / decode 
            for i in range(0, len(bline)):
                char = struct.unpack('B', bline[i])[0]
                out = (char ^ 129 + ~(i * 21 + 1)) & 0xFF
                tmp += struct.pack('B', out)

            #put it back in the right format
            if not decode:
                tmp = binascii.hexlify(tmp)
                tmp += '\r\n'
    print tmp
    fd = open(outfile, 'wb')
    fd.write(tmp)
    fd.close()


def usage():
    print 'encode/decode WumConfig.txt file'
    print sys.argv[0], "infile outfile"


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
        exit()
    else:
        main()    
