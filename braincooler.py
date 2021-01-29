import sys
from subprocess import call

def openFile(path):
    return open(path, 'r')

def openOutput():
    return open('output.asm', 'w')

def removeComments(content):
    rv = ""
    for i in content:
        if i == '>' or i == '<' or i == '+' or i == '-' or i == '.' or i == ',' or i == '[' or i == ']':
            rv += i
    return rv

def incPtr(file):
    file.write("\tinc esi\n")

def decPtr(file):
    file.write("\tdec esi\n")

def inc(file):
    file.write("\tadd BYTE PTR [esi], 1\n")

def dec(file):
    file.write("\tsub BYTE PTR [esi], 1\n")

def printChar(file):
    file.write("\tmov ecx, esi\n")
    file.write("\tmov eax, 4\n")
    file.write("\tmov ebx, 1\n")
    file.write("\tmov edx, 1\n")
    file.write("\tint 0x80\n")

def getChar(file):
    file.write("\tmov ecx, esi\n")
    file.write("\tmov eax, 3\n")
    file.write("\tmov ebx, 0\n")
    file.write("\tmov edx, 1\n")
    file.write("\tint 0x80\n") 

def loopStart(file, jump):
    file.write("\tmov bl, BYTE PTR [esi]\n")
    file.write("\tcmp bl, 0\n")
    file.write("\tjz label"+str(jump[1]) + "\n")
    file.write("label" + str(jump[0]) + ":\n")

def loopEnd(file, jump):
    file.write("\tmov bl, BYTE PTR [esi]\n")
    file.write("\tcmp bl, 0\n")
    file.write("\tjnz label" + str(jump[0]) + "\n")
    file.write("label" + str(jump[1]) + ":\n")

def compile(file, content, jumptable):
    stack = []
    index = -1
    start(file)
    for i in content:
        if i == '>':
            incPtr(file)
        elif i == '<':
            decPtr(file)
        elif i == '+':
            inc(file)
        elif i == '-':
            dec(file)
        elif i == '.':
            printChar(file)
        elif i == ',':
            getChar(file)
        elif i == '[':
            index += 1
            stack.append(jumptable[index])
            loopStart(file, stack[-1])
        elif i == ']':
            loopEnd(file, stack[-1])
            stack.pop()            
    end(file)

def start(file):
    file.write(".intel_syntax noprefix\n")
    file.write(".text\n")
    file.write(".globl _start\n")
    file.write("_start:\n")
    file.write("\tmov esi, offset buffer\n")

def end(file):
    file.write("\tmov eax, 1\n")
    file.write("\tint 0x80\n")
    file.write("\n")
    file.write(".bss\n")
    file.write("\t.comm buffer, 30000, 32\n") 

def createJumpTable(content):
	jt = []
	l = 0 #Current label
	ltc = [] #Label to close
	for i in content:
		if i == '[':
			l += 1
			ltc.append(l)
		elif i == ']':
			l += 1
			jt.append([ltc.pop(), l])
	jt = sorted(jt, key=lambda jt: jt[0])	
	return jt

def assembleAndLink():
    call(["as", "--32", "output.asm", "-o", "output.o"])
    call(["ld", "-m", "elf_i386", "output.o"])

# Open bf file 
file = openFile(sys.argv[1])

# Open the output.asm file
outputfile = openOutput()

# Get the bf file content
content = ""
for line in file:
    content += line.strip()

# Close the bf file
file.close()

# Remove comments from the content
content = removeComments(content)

# Recreate jump table
jt = createJumpTable(content)

# Compile and write asm to output.asm
compile(outputfile, content, jt)

# Close the output file
outputfile.close()

# Assemble and link
assembleAndLink()
