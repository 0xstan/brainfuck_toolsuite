#!/usr/bin/env python

import sys
import curses
from curses import wrapper
import time

class Program:
	def __init__(self, file):	
		self.text = ''
		self.reset()
		self.bp = {}
		bffile = open(file, "r")		
		content = bffile.read()
		## Remove comments
		for i in content:
			if i == '>' or i == '<' or i == '+' or i == '-' or i == '.' or i == ',' or i == '[' or i == ']':
				self.text += i	
	def reset(self):
		self.data = [0]*30000
		self.eip = 0
		self.esi = 0
		self.input = b'' ## Buffer for user input
		self.index = 0 ##Index for loops
		self.running = False ## Is running
		self.cont = False ## Used for breakpoints
	
	def breakpoint(self, gui):
		set = True
		## Get eip under the cursor
		curse = (gui.codecursor[0] + gui.linetext)*gui.CODE_WIDTH + gui.codecursor[1]
		## if eip already in bp, unset it
		if curse in self.bp:
			set = False
		## Cursor can be outside code
		if curse >= len(self.text):
			return
		## Set bp
		if set:
			self.bp[curse] = self.text[curse]
		## Unset it
		else:
			del self.bp[curse]

	def run(self, gui):
		## Run the program, stop at the end, or when reaching bp
		self.reset()
		self.running = True
		while(self.eip < len(self.text)) and self.running:
			self.execone(gui)

	def continueexec(self, gui):
		self.running = True
		## Cont = true means that current Bp will be passed
		self.cont = True
		while(self.eip < len(self.text)) and self.running:
			self.execone(gui)

	def execone(self, gui):
		if (self.eip in self.bp) and not self.cont:
			self.running = False
			return
		self.running = 1
		self.cont = False
		if self.text[self.eip] == '>':
			self.esi += 1
			self.esi %= 30000
			self.eip += 1
		elif self.text[self.eip] == '<':
			self.esi -= 1
			self.esi %= 30000
			self.eip += 1
		elif self.text[self.eip] == '+':
			self.data[self.esi] += 1
			self.data[self.esi] %= 256
			self.eip += 1
		elif self.text[self.eip] == '-':
			self.data[self.esi] -= 1
			self.data[self.esi] %= 256
			self.eip += 1
		elif self.text[self.eip] == '.':
			try:
				gui.user.addch(chr(self.data[self.esi]))
			except curses.error:
				gui.user.clear()
			gui.user.refresh()
			self.eip += 1
		elif self.text[self.eip] == ',':
			if self.input == b'':
				gui.focus = gui.user
				gui.writeinfo(self)
				gui.action(self)
				gui.focus = gui.code
				gui.writeinfo(self)
			self.data[self.esi] = self.input[0]
			self.input = self.input[1:]
			self.eip += 1				
		elif self.text[self.eip] == '[':
			if self.data[self.esi] == 0:
				self.index += 1
				while self.index:
					self.eip += 1
					if self.text[self.eip] == '[':
						self.index += 1
					elif self.text[self.eip] == ']':
						self.index -= 1
				self.eip += 1
			else:
				self.eip += 1
		elif self.text[self.eip] == ']':
			if self.data[self.esi] != 0:
				self.index += 1
				while self.index:
					self.eip -= 1
					if self.text[self.eip] == '[':
						self.index -= 1
					elif self.text[self.eip] == ']':
						self.index += 1
				self.eip += 1
			else:
				self.eip += 1
		if self.eip == len(self.text):
			self.running = True

class Gui:
	def __init__(self):
		self.CODE_WIDTH = 100
		self.CODE_HEIGHT = 10
		
		self.USER_WIDTH = 100
		self.USER_HEIGHT = 10
		
		self.DATA_WIDTH = 100
		self.DATA_HEIGHT = 10

		self.INFO_WIDTH = 30
		self.INFO_HEIGHT = 17

		self.stdscr = curses.initscr()
		curses.noecho()
		curses.cbreak()
		
		curses.start_color()
		## EIP
		curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
		## Breakpoint
		curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
		## Breakpoint + EIP
		curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_RED)
		## Normal
		curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

		self.code = curses.newwin(self.CODE_HEIGHT, self.CODE_WIDTH, 0, 0)
		self.code.keypad(True)
		
		self.user = curses.newwin(self.USER_HEIGHT, self.USER_WIDTH, 15, 0)

		self.data = curses.newwin(self.DATA_HEIGHT, self.DATA_WIDTH, 30, 0)
		self.data.keypad(True)

		self.info = curses.newwin(self.INFO_HEIGHT, self.INFO_WIDTH, 0, 110)
		self.info.border()

		self.linetext = 0
		self.focus = self.code
		self.codecursor = [0,0]
		self.datacursor = 0

	def writeinfo(self, program):
		self.info.clear()
		self.info.addstr(1, 1, "Commands:")
		self.info.addstr(2, 2, "Arrows: Move cursor")
		self.info.addstr(3, 2, "r: run")
		self.info.addstr(4, 2, "c: continue")
		self.info.addstr(5, 2, "b: set breakpoint")
		self.info.addstr(6, 2, "n: step")
		self.info.addstr(7, 2, "q: quit")
		self.info.addstr(8, 2, "f: reset prog")
		self.info.addstr(9, 2, "TAB: change window")
		self.info.addstr(10, 2, "Current window: ")
		if self.focus == self.user:
			self.info.addstr(10, 18, "user")
		elif self.focus == self.code:
			self.info.addstr(10, 18, "code")
		elif self.focus == self.data:
			self.info.addstr(10, 18, "data")
		
		self.info.addstr(12, 1, "Program:")
		self.info.addstr(13, 2, "esi: " + str(program.esi))
		self.info.addstr(14, 2, "[esi]: " + str(program.data[program.esi]))	
		self.info.addstr(15, 2, "eip: " + str(program.eip))
		
		self.info.refresh()

	def writecode(self, program):
		self.code.clear()
		
		## end is the last eip printed in the window
		## if this eip < last instr of program, it's OK
		## else, we set it to the last instr
		end = int((self.linetext + self.CODE_HEIGHT)*self.CODE_WIDTH)
		if len(program.text) < end:
			end = int(len(program.text))

		## write instr
		self.code.move(0, 0)
		for i in range(self.linetext*self.CODE_WIDTH, end):	
			if i == program.eip and (i in program.bp):
				attr = curses.color_pair(3)
			elif i == program.eip:
				attr = curses.color_pair(1)
			elif i in program.bp:
				attr = curses.color_pair(2)
			else:
				attr = curses.color_pair(4)
			self.code.attron(attr)
			## shitty curses, this is only for the char in the right-down corner
			try:
				self.code.addch(program.text[i])
			except curses.error:
				pass
		## Go back to the user cursor
		self.code.move(self.codecursor[0], self.codecursor[1])
		self.code.refresh()	

	def writedata(self, program):
		self.data.clear()
		for i in range(self.DATA_HEIGHT):
			self.data.addstr(i, 0, str((self.datacursor + i)*12) + ":")
			for j in range(12):
				if ((self.datacursor+i)*12 + j) == program.esi:
					self.data.attron(curses.color_pair(1))
					self.data.addstr(i, 8*(j + 1), str(program.data[int((self.datacursor+i)*12 + j)]))
					self.data.attroff(curses.color_pair(1))
				else:
					self.data.addstr(i, 8*(j + 1), str(program.data[int((self.datacursor+i)*12 + j)]))
		self.data.refresh()

	def teardown(self):
		## End debugger
		curses.nocbreak()
		self.stdscr.keypad(False)
		curses.echo()
		curses.endwin()

	def writeall(self, program):
		self.writeinfo(program)
		self.writecode(program)
		self.writedata(program)

	def action(self, program):
		## Dispatcher
		if self.focus == self.code:
			self.actioncode(program)
		elif self.focus == self.data:
			self.actiondata(program)
		elif self.focus == self.user:
			self.actionuser(program)

	def actioncode(self, program):
		c = self.code.getch()
		## Keys for managing the user cursor, not really difficult (codecursor[0] for y, codecursor[1] for x)
		if c == curses.KEY_LEFT:
			if self.codecursor[1] > 0:
				self.codecursor[1] -= 1
				self.code.move(self.codecursor[0], self.codecursor[1])
		elif c == curses.KEY_RIGHT:
			if self.codecursor[1] < (self.CODE_WIDTH - 1):
				self.codecursor[1] += 1
				self.code.move(self.codecursor[0], self.codecursor[1])
		elif c == curses.KEY_UP:
			if self.codecursor[0] == 0 and self.linetext > 0:
				self.linetext -= 1
				self.writecode(program)
			elif self.codecursor[0] > 0:
				self.codecursor[0] -= 1
				self.code.move(self.codecursor[0], self.codecursor[1])
		elif c == curses.KEY_DOWN:
			if (self.codecursor[0] == (self.CODE_HEIGHT - 1)) and (len(program.text) > (self.linetext + self.CODE_HEIGHT)*self.CODE_WIDTH):
				self.linetext += 1
				self.writecode(program)
			elif self.codecursor[0] < (self.CODE_HEIGHT - 1):
				self.codecursor[0] += 1
				self.code.move(self.codecursor[0], self.codecursor[1])
		elif c == ord('r'):
			self.user.clear()
			program.run(self)
			gui.writeall(program)
		elif c == ord('c'):	
			program.continueexec(self)
			gui.writeall(program)
		elif c == ord('f'):
			program.reset()
			self.user.clear()
			self.user.refresh()
		elif c == ord('n'):
			program.cont = 1
			if (program.eip < len(program.text)):
				program.execone(self)	
				gui.writeall(program)
		elif c == ord('b'):
			program.breakpoint(gui)
			gui.writecode(program)
		elif c == ord('q'):
			self.teardown()
			sys.exit()
		elif c == 9:
			self.focus = self.data
			self.writeinfo(program)

	def actiondata(self, program):
		c = self.code.getch()
		if c == ord('q'):
			self.teardown()
			sys.exit()
		elif c == curses.KEY_UP:
			if self.datacursor > 0:
				self.datacursor -= 1
				self.writedata(program)
		elif c == curses.KEY_DOWN:
			# 12 bytes by lines, 10 lines printed. so 2500 lines, max datacursor = 2490 (last line is 2500)
			if (self.datacursor < (30000/12) - self.DATA_HEIGHT):
				self.datacursor += 1
				self.writedata(program)
		elif c == 9:
			self.focus = self.code
			self.writeinfo(program)

	def actionuser(self, program):
		curses.nocbreak()
		curses.echo()
		program.input = self.focus.getstr()
		program.input += b'\n'
		curses.noecho()
		curses.cbreak()

if __name__ == "__main__":
	program = Program(sys.argv[1])
	gui = Gui()
	gui.writeinfo(program)	
	gui.writedata(program)
	gui.writecode(program)
	while True:
		gui.action(program)
