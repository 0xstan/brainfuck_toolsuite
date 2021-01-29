import sys

def openandread(filepath):
	bffile = open(filepath, "r")
	content = bffile.read()
	program = ''
	for i in content:
		if i == '>' or i == '<' or i == '+' or i == '-' or i == '.' or i == ',' or i == '[' or i == ']':
			program += i
	return program	 

def execbf(program):
	inputuser = ''
	eip = 0
	data = [0]*30000
	esi = 0
	index = 0
	while(eip < len(program)):
		if program[eip] == '>':
			esi += 1
			esi %= 30000
			eip += 1
		elif program[eip] == '<':
			esi -= 1
			esi %= 30000
			eip += 1
		elif program[eip] == '+':
			data[esi] += 1
			data[esi] %= 256
			eip += 1
		elif program[eip] == '-':
			data[esi] -= 1	
			data[esi] %= 256
			eip += 1
		elif program[eip] == '.':
			print(chr(data[esi]), end='')
			eip += 1
		elif program[eip] == ',':
			if inputuser == '':
				inputuser = input()
				inputuser += '\n'
			data[esi] = ord(inputuser[0])
			inputuser = inputuser[1:]
			eip += 1
		elif program[eip] == '[':
			if data[esi] == 0:
				index += 1
				while index:
					eip += 1
					if program[eip] == '[':
						index += 1
					elif program[eip] == ']':
						index -= 1
				eip += 1
			else:
				eip += 1
		elif program[eip] == ']':
			if data[esi] != 0:
				index += 1
				while index:
					eip -= 1
					if program[eip] == '[':
						index -= 1
					elif program[eip] == ']':
						index += 1
				eip += 1
			else:
				eip += 1
	

if __name__ == "__main__" :
	program = openandread(sys.argv[1])
	execbf(program)
