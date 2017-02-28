import sys
import os

# Display help message
def usage():
	print("Usage: %s namefile.asm" % os.path.basename(sys.argv[0]))
	print("-h	Help")
	print("-l	Output to Logisim binary image")
	print("-b	Output to raw binary image")

# List of valid opcodes (in order)
opcodes = [ "LDI",
			"STM",
			"LDM",
			"LDMA",
			"ADDI",
			"SUBI",
			"ADDM",
			"SUBM",
			"JMPI",
			"JMPM",
			"JMPA",
			"JMPMA",
			"JZI",
			"JCI",
			"OUT",
			"HLT" ]

# Number of opperands each opcode takes (in same order as opcode list so we can do a lookup)
opperands = ["d","a","a",0,"d","d","a","a","a","a",0,0,"a","a",0,0]

# Arrays for labels and addresses
labels = []
labelValues = []

# Arrays for labels and addresses
constants = []
constantValues = []

# Array of lines for second stage to process
tempFile = []

# Output array
binaryOut = []

def main():
	# Command line argument handling
	args = sys.argv[1:]
	if "-h" in args or "--help" in args or args==[]:
		usage()
		sys.exit(2)

	# Open source file
	file = open(args[0],"r")

	# First pass
	addr = 0
	#print("First pass")
	
	for line in file:
		line = line.strip()
		line = line.rstrip('\r\n')
		
		if len(line) < 2:
			continue

		# Check if the line is a comment
		elif line[0] == "/" and line[1] == "/":
			continue
		
		# Check if the line is a label and add to array for reference in second pass
		elif line[-1:] == ":":
				#print("Found label: %s at %02x" % (line[:-1],addr))
				labels.append(line[:-1])
				labelValues.append(addr)
				continue
		
		elif len(line.split(" ")) > 2 and line.split(" ")[1] == "EQU":
				#print("Found constant: %s = %s" % (line.split(" ")[0],line.split(" ")[2]))
				constants.append(line.split(" ")[0])
				constantValues.append(line.split(" ")[2])
				continue
		
		for const in constants:
			if const in line and line.split(" ")[1] != "EQU":
				line = line.replace(const, str(constantValues[constants.index(const)]))
				
		if "$" in line:
			line = line.replace("$", str(addr))
		
		# If opcode or data byte then increment address and add to tempFile
		if line.split(" ")[0] in opcodes or line.split(" ")[0] == "db":
				addr += 1
				tempFile.append(line)
	
	# Second Pass
	addr = 0
	#print("Second pass")
	
	for line in tempFile:
		
		# Check if address is in range (0x0 - 0xF)
		if addr < 0x0 or addr > 0xF:
			print("Address out of range: %02x" % addr)
			sys.exit(1)
			
		else:
			# Get mnemonic
			mnemonic = line.split(" ")[0]
			
			# Check if mnemonic is valid
			if mnemonic in opcodes:
				opcode = opcodes.index(mnemonic)
				
				# Check if it takes an opperand
				if opperands[opcodes.index(mnemonic)] != 0:
					
					# Get opperand
					opperand = line.split(" ")[1]
					
					# Check to see if label and if opcode takes address
					if opperand in labels and opperands[opcodes.index(mnemonic)] == "a":
						opperand = labelValues[labels.index(opperand)]
					
					# Otherwise parse to int
					else:
						try:
							opperand = int(opperand,0)
						except:
							print("Invalid opperand: %s" % opperand)
							sys.exit(1)
					
					# Check opperand is in range (0x0-0xF)
					if opperand < 0x0 or opperand > 0xF:
						print("Opperand out of range: %02x" % opperand)
						sys.exit(1)
						
				# If it doesn't take an opperand just default to 0
				else:
					opperand = 0
					
				# Combine opcode and opperand to get final hex value
				hexout = (opcode<<4) | opperand
				
			# If not a valid mnemonic check if it is a data byte
			else:
				if mnemonic == "db":
					
					hexout = int(line.split(" ")[1],0)
					
					# Check data is in range (0x00 - 0xFF)
					if hexout < 0x00 or hexout > 0xFF:
						print("Data out of range: %02x" % hexout)
						sys.exit(1)
						
				else:
					# If it wasn't a valid opcode or a data byte then it must be an invalid opcode so exit
					print("Invalid Mnemonic: %s" % mnemonic)
					sys.exit(1)
					
			# Print, append to output array and increment address
			print("%01x: %02x" % (addr, hexout))
			binaryOut.append(hexout)
			addr += 1
	
	# Output to Logisim binary image
	if "-b" in args:
		print("Converting to raw binary image...")
		newFile = open("%s.bin" % args[0].split(".")[0] , "w")
		newFileBytes = []
		for val in binaryOut:
			newFileBytes.append(val)
		newFileByteArray = bytearray(newFileBytes)
		newFile.write(newFileByteArray)
		print("Success!")
	
	# Output to Logisim binary image
	if "-l" in args:
		print("Converting to Logisim binary image...")
		newFile = open("%s.lbi" % args[0].split(".")[0] , "w")
		newFileBytes = ["v", "2", ".", "0", 0x20, "r", "a", "w", 0x0A]
		for val in binaryOut:
			newFileBytes.append(("%02x" % val)[0])
			newFileBytes.append(("%02x" % val)[1])
			newFileBytes.append(0x20)
		newFileBytes.append(0x0A)
		newFileByteArray = bytearray(newFileBytes)
		newFile.write(newFileByteArray)
		print("Success!")
		
if __name__ == "__main__":
	main()
