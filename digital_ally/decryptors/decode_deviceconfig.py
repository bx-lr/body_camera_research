import struct
import sys


def main():
    #sweet encryption bro...
    #// DigitalAlly.Devices.Configuration.DeviceConfigurationFile
    '''
	private static void Encode(byte[] buffer, int byteCnt)
	{
		for (int i = 0; i < byteCnt; i += 8)
		{
			long num = BitConverter.ToInt64(buffer, i);
			num ^= 0x7777777777777777;
			num = ~num;
			byte[] bytes = BitConverter.GetBytes(num);
			bytes.CopyTo(buffer, i);
		}
	}

    '''

    infile = sys.argv[1]
    outfile = sys.argv[2]
    fd = open(infile, 'rb')
    data = fd.read()
    fd.close()
    
    
    tmp = ''
    for d in data:
        #really we could just xor each byte with 0x88
        #but we will do this to keep in line with what they
        #are doing
        c = struct.unpack('B', d)[0]
        #print c
        c ^= 0x77
        #print hex(c)
        c = ~c
        #print hex(c)
        c = c & 0xff
        #print hex(c)
        tmp += struct.pack('B',c)
    
    fd = open(outfile, 'wb')
    fd.write(tmp)
    fd.close()

def usage():
    print 'encode/decode deviceconfig file'
    print sys.argv[0], "infile outfile"


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
        exit()
    else:
        main()
