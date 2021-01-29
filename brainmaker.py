## Must be set to 8 or 16 before calling functions 
BITS_MODE = 8

#This function write the string at ptr+1, ptr must contain a 0, stop at the end of string (0), then go move backward to ptr
def writeCells():
  prog = moveForward()
  prog += whileStart()
  prog += writeCell()
  prog += moveForward()
  prog += whileEnd()
  prog += moveBackward()
  prog += whileStart()
  prog += moveBackward()
  prog += whileEnd()
  return prog

def writeCell():
  if BITS_MODE == 8:
    return '.'
  elif BITS_MODE == 16:
    return '>>.<<'

def getCell():
  if BITS_MODE == 8:
    return ','
  elif BITS_MODE == 16:
    return '>>,>[-]<<<'

def moveForward():
  if BITS_MODE == 8:
    return '>'
  elif BITS_MODE == 16:
    return '>>>>'

def moveBackward():
  if BITS_MODE == 8:
    return '<'
  elif BITS_MODE == 16:
    return '<<<<'

#dec
def decCell():
  if BITS_MODE == 8:
    return '-'
  elif BITS_MODE == 16:
    return '>+>[<-]<[->>-<<<]>>-<<'

#inc
def incCell():
  if BITS_MODE == 8:
    return '+'
  elif BITS_MODE == 16:
    return '>>+<+>[<-]<[->>+<<<]'

#while block
def whileStart():
  if BITS_MODE == 8:
    return '['
  elif BITS_MODE == 16:
    return '>>>[[->+<]<<+>>]<[[->+<]<+>]>[-<+>]>[-<+>]<<<[[-]<'

def whileEnd():
  if BITS_MODE == 8:
    return ']'
  elif BITS_MODE == 16:
    return '>>>[[->+<]<<+>>]<[[->+<]<+>]>[-<+>]>[-<+>]<<<]<'

#goto new when ptr = current
def gotoPtr(current, new):
  prog = ''
  if current > new:
    for i in range(0, current - new):
      prog += moveBackward()
  else:
    for i in range(0, new - current):
      prog += moveForward()
  return prog

#writeString, use 1 cell, at the end, the cell contain the last char
def writeString(string):
  prec = 0
  prog = ''
  prog += cleanCell()
  for i in string:
    if ord(i)-prec >= 0:
      for j in range(0, ord(i) - prec):
        prog += incCell()
    else:
      for j in range(0, prec - ord(i)):
        prog += decCell()
    prog += writeCell()
    prec = ord(i)
  return prog

#store the array at ptr + 1, and clean ptr
def store(array):
  prog = ''
  prog += cleanCell()
  prog += moveForward()
  for i in array:
    for j in range(0, i):
      prog += incCell()
    prog += moveForward()
  for j in range(0, len(array) + 1):
    prog += moveBackward()
  return prog

#get line at ptr+1, ptr must contain a 0 !
def getLine():
  prog = ''
  prog += incCell()
  prog += whileStart()
  prog += decCell()
  prog += moveForward()
  prog += getCell()
  for i in range(0, 10):
    prog += decCell()
  prog += whileEnd()
  prog += moveBackward()
  prog += whileStart()
  for i in range(0, 11):
    prog += incCell()
  prog += moveBackward()
  prog += whileEnd()
  return prog

# this if block (code executed if cell != 0)  is destructive (at the end cell == 0)
def startIfPtr():
  prog = whileStart()
  return prog 

def endIfPtr():
  prog = ''
  prog += cleanCell()
  prog += whileEnd()
  return prog

#Assume that value1 is in ptr, value2 in ptr+1, result in ptr
def addbf():
  prog = ''
  prog += moveForward()
  prog += whileStart()
  prog += moveBackward()
  prog += incCell()
  prog += moveForward()
  prog += decCell()
  prog += whileEnd()
  prog += moveBackward()
  return prog

def subbf():
  prog = ''
  prog += moveForward()
  prog += whileStart()
  prog += moveBackward()
  prog += decCell()
  prog += moveForward()
  prog += decCell()
  prog += whileEnd()
  prog += moveBackward()
  return prog

# A   B 0 0
# AxB 0 0 0
# [->[->+>+<<]>[-<+>]<<]>[-]>>[-<<<+>>>]<<<
def mulbf():
  prog = ''
  prog += whileStart()
  prog += decCell()
  prog += moveForward()
  prog += whileStart()
  prog += decCell()
  prog += moveForward()
  prog += incCell()
  prog += moveForward()
  prog += incCell()
  prog += moveBackward()
  prog += moveBackward()
  prog += whileEnd()
  prog += moveForward()
  prog += whileStart()
  prog += decCell()
  prog += moveBackward()
  prog += incCell()
  prog += moveForward()
  prog += whileEnd()
  prog += moveBackward()
  prog += moveBackward()
  prog += whileEnd()
  prog += moveForward()
  prog += whileStart()
  prog += decCell()
  prog += whileEnd()
  prog += moveForward()
  prog += moveForward()
  prog += whileStart()
  prog += decCell()
  prog += moveBackward()
  prog += moveBackward()
  prog += moveBackward()
  prog += incCell()
  prog += moveForward()
  prog += moveForward()
  prog += moveForward()
  prog += whileEnd()
  prog += moveBackward()
  prog += moveBackward()
  prog += moveBackward()
  return prog

# Does not works in 16 bits !!! don't know why
#Assume that ptr is nul, val1 is in ptr+1 and val2 in ptr+2. result in ptr+2. comsume 30 cells !!
def xorbf():
  prog = ''
  prog += moveForward()
  prog += moveForward()
  prog += moveForward()
  for j in range(27):
    prog += moveForward()
    prog += cleanCell()
  for j in range(0, 30):
    prog += moveBackward()
  prog += decCell()
  prog += whileStart()
  prog += whileStart()
  for j in range(0, 6):
    prog += moveForward()
  prog += whileStart()
  for j in range(0, 3):
    prog += moveForward()
  prog += whileEnd()
  prog += incCell()
  prog += incCell()
  prog += whileStart()
  prog += decCell()
  for j in range(0, 3):
    prog += moveBackward()
  prog += whileEnd()
  for j in range(0, 3):
    prog += moveBackward()
  prog += decCell()
  prog += whileEnd()
  prog += moveForward()
  prog += whileEnd()
  for j in range(0, 3):
    prog += moveForward()
  prog += whileStart()
  prog += moveBackward()
  prog += whileEnd()
  prog += moveForward()
  prog += whileStart()
  prog += whileStart()
  prog += moveForward()
  prog += whileStart()
  prog += moveForward()
  prog += decCell()
  prog += moveBackward()
  prog += decCell()
  prog += whileEnd()
  prog += moveForward()
  prog += whileStart()
  for j in range(0, 6):
    prog += moveBackward()
  prog += incCell()
  for j in range(0, 6):
    prog += moveForward()
  prog += cleanCell()
  prog += whileEnd()
  prog += moveForward()
  prog += whileEnd()
  prog += incCell()
  prog += whileStart()
  prog += moveBackward()
  prog += whileStart()
  for j in range(0, 3):
    prog += moveBackward()
  prog += incCell()
  prog += incCell()
  for j in range(0, 3):
    prog += moveForward()
  prog += decCell()
  prog += whileEnd()
  prog += moveBackward()
  prog += moveBackward()
  prog += whileEnd()
  prog += moveForward()
  prog += moveForward()
  prog += whileEnd()
  prog += moveBackward()
  prog += moveBackward()
  prog += moveBackward()
  prog += moveBackward()
  prog += moveBackward()
  return prog

def modulus(): 
  # 0 >n 0 d 0 0 0
  # [>+>->+<[>]>[<+>-]<<[<]>-]
  # 0 >0 n d-n%d n%d 0 0
  prog = ''
  prog += whileStart()
  prog += moveForward()
  prog += incCell()
  prog += moveForward()
  prog += decCell()
  prog += moveForward()
  prog += incCell()
  prog += moveBackward()
  prog += whileStart()
  prog += moveForward()
  prog += whileEnd()
  prog += moveForward()
  prog += whileStart()
  prog += moveBackward()
  prog += incCell()
  prog += moveForward()
  prog += decCell()
  prog += whileEnd()
  prog += moveBackward()
  prog += moveBackward()
  prog += whileStart()
  prog += moveBackward()
  prog += whileEnd()
  prog += moveForward()
  prog += decCell()
  prog += whileEnd()
  return prog


#this if/else block (if(x != 0), else) is non destructive and consume 3 cells
def ifInIfElse():
  prog = ''
  prog += moveForward()
  prog += cleanCell() 
  prog += incCell()
  prog += moveForward()
  prog += cleanCell()
  prog += moveBackward()
  prog += moveBackward()
  prog += whileStart()
  return prog

#ptr is on x
def elseInIfElse():
  prog = ''
  prog += moveForward()
  prog += decCell()
  prog += whileEnd()
  prog += moveForward()
  prog += whileStart()
  prog += moveBackward()
  return prog

##ptr is on x
def endIfElse():
  prog = ''
  prog += moveForward()
  prog += decCell()
  prog += moveForward()
  prog += whileEnd()
  prog += moveBackward()
  prog += moveBackward()
  return prog

##put 1 in current cell
def put1():
  prog = ''
  prog += cleanCell()
  prog += incCell()
  return prog

#put 0 in current cell
def cleanCell():
  prog = ''
  prog += whileStart()
  prog += decCell()
  prog += whileEnd()
  return prog

#copy value in src to dest, use temp cell at dest+1 (dest and dest+1 must be 0 at start !), assume ptr is on src (non destructive)
# if src and dest aren't defined, copycell from ptr to ptr-1 (destructive)
def copyCell(src = -1, dest = -1):
  prog = ''
  
  if src == -1 or dest == -1:
    prog += whileStart()
    prog += decCell()
    prog += moveBackward()
    prog += incCell()
    prog += moveForward()
    prog += whileEnd()
    return prog
  else:
    prog += whileStart()
    prog += decCell()
    # copy src in dest AND dest+1 (src <= dest) src is 0 at the end of loop
    if (src <= dest):
      for i in range(0, dest - src):
        prog += moveForward()
      prog += incCell()
      prog += moveForward()
      prog += incCell()
      for i in range(0, dest - src + 1):
        prog += moveBackward()
    # dest < src
    else:
      for i in range(0, src - dest):
        prog += moveBackward()
      prog += incCell()
      prog += moveForward()
      prog += incCell()
      for i in range(0, src - dest - 1):
        prog += moveForward()
    prog += whileEnd()
    prog += gotoPtr(src, dest+1)
    prog += whileStart()
    prog += decCell()
    # copy back dest+1 into src, dest+1 is 0 at the end
    if (src <= dest):
      for i in range(0, dest - src + 1):
        prog += moveBackward()
      prog += incCell()
      for i in range(0, dest - src + 1):
        prog += moveForward()
    else:
      for i in range(0, src - dest - 1):
        prog += moveForward()
      prog += incCell()
      for i in range(0, src - dest - 1):
        prog += moveBackward()
    prog += whileEnd()  
    prog += gotoPtr(dest+1, src)
    return prog
