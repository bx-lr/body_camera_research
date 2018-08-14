from Crypto.Cipher import AES
#import Crypto.Cipher.AES
import xml.etree.cElementTree as ET
import base64
import sys

#// DigitalAlly.Security.Cryptography.XmlEncryption


def main():
    #yes we are getting the crypto key from the filename /facepalm
    name = sys.argv[1]
    name = name.split('.')[0]

    #this is just embarrassing
    pw_iv = ''
    pw_iv += name[2:4]
    pw_iv += name[12:14]
    pw_iv += name[10:12]
    pw_iv += name[16:18]
    
    key = ''
    #unicode hax
    for c in pw_iv:
        key += c
        key += '\x00'

    #yes key and iv are the same
    IV = key
    cipher = AES.new(key,AES.MODE_CBC,IV)


    #get the xml element with encrypted data
    tree = ET.parse(sys.argv[1])
    for elem in tree.iter():
        #ugly but meh
        if str(elem.tag) == '{http://www.w3.org/2001/04/xmlenc#}CipherValue':
            data = elem.text

    #oh noes!
    if len(data) < 1:
        print 'Cant find CipherValue! Quitting!'
        return

    #base64 decode and decrypt the ciphervalue
    blob = base64.b64decode(data)
    tmp = cipher.decrypt(blob)

    #write out the decrypted data
    fd = open(sys.argv[2], 'wb')
    fd.write(tmp)
    fd.close()

    #write out the key used to decrypt the contents
    fd = open(sys.argv[2] + '.key', 'wb')
    fd.write(key)
    fd.close()
    print 'Done! Check:', sys.argv[2]
    print 'Done! Check:', sys.argv[2] + '.key'

def usage():
    print 'decrypt *.vm2 file CipherValue'
    print sys.argv[0], "infile outfile"


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
        exit()
    else:
        main()    

