// 0x0 LDI
// 0x1 STM
// 0x2 LDM
// 0x3 LDMA
// 0x4 ADDI
// 0x5 SUBI
// 0x6 ADDM
// 0x7 SUBM
// 0x8 JMPI
// 0x9 JMPM
// 0xA JMPA
// 0xB JMPMA
// 0xC JZM
// 0xD JCM
// 0xE OUT
// 0xF HLT
// $ = Current Address

JMPI Start
Start:
	LDI 0
Loop:
	ADDI 1
	OUT
	JMPI Loop