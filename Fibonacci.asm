// 0x0x LDI	Load immediate
// 0x1x STM	Store memory
// 0x2x LDM	Load memory
// 0x3x LDMA	Load memory indexed by A
// 0x4x ADDI	Add immediate
// 0x5x SUBI	Sub immediate
// 0x6x ADDM	Add memory
// 0x7x SUBM	Sub memory
// 0x8x JMPI	Jump immediate
// 0x9x JMPM	Jump memory
// 0xAx JMPA	Jump A
// 0xBx JMPMA	Jump memory indexed by A
// 0xCx JZI	Jump zero immediate
// 0xDx JCI	Jump carry immediate
// 0xEx OUT	Output
// 0xFx HLT	Halt
// $ = Current Address

Init:
LDI 1
STM A
STM B

Start:
ADDM A
STM A
JCI $
OUT
LDM A

ADDM B
STM B
JCI $
OUT
LDM B
JMPI Start

// Vars
A:
db 0x1
B:
db 0x1
