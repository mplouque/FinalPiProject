##############################################################################################
# Name: Pablo Johnson
# Description: python script to take in input file and either encode it or decode it to base64
# Made for ABKMP Final Pi Project for Cyberstorm 2016
##############################################################################################

import base64, os, sys 

# define our encoding function, passing in our incoming and outgoing files
def encoder(incoming,outgoing):
	unencoded_file = open(incoming, 'r')
	encoded_string = base64.b64encode(unencoded_file.read())
	foo = open(outgoing,'wb+')
	foo.write(encoded_string)
	foo.close()
	unencoded_file.close()

def decoder(incoming, outgoing):
	encoded_file = open(incoming, 'r')
	unencoded_string = base64.b64decode(encoded_file.read())
	foo = open(outgoing, 'wb+')
	foo.write(unencoded_string)
	foo.close()
	encoded_file.close()

if (len(sys.argv) < 4):
	print "Usage is <e/d> <input_file> <output_file>\nWith <e/b> being either e for encode or d for decode" 
	exit()

input_file= sys.argv[2]
output_file = sys.argv[3]

if (sys.argv[1] == 'd'):
	print 'Decoding {} to {}.'.format(input_file, output_file)
	decoder(input_file,output_file)
elif (sys.argv[1] == 'e'):
	print 'Encoding {} to {}.'.format(input_file, output_file)
	encoder(input_file,output_file)
else:
	print "Usage is <e|d> <input_file> <output_file>\nWith <e|b> being either e for encode or d for decode" 
	exit()


print 'Done'
