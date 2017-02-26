# Homebrew CPU
This a simple CPU implemented in Logisim, inspired by the SAP-1 architecture featured in the book "Digital Computer Electronics" by Albert Paul Malvino.

##Instruction Set:
* LDI   -  Load immediate
* STM   -  Store to memory
* LDM   -  Load from memory
* LDMA  -  Load from memory pointed to by A
* ADDI  -  Add immediate
* SUBI  -  Sub immediate
* ADDM  -  Add from memory
* SUBM  -  Sub from memory
* JMPI  -  Jump to immediate address
* JMPM  -  Jump to address stored in memory
* JMPA  -  Jump to address stored in A
* JMPMA -  Jump to address stored in memory pointed to by A
* JZI   -  Jump to immediate address if Zero flag set
* JCI   -  Jump to immediate address if Carry flag set
* OUT   -  Output the value stored in A
* HLT   -  Halt

## Assembler Features
* Hex, binary and decimal values
* Labels
* Constants
* $ represents current address
* Data bytes
* Can output to raw binary or Logisim binary image file
