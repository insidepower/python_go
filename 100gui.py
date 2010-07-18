import appuifw, e32, graphics
import sysinfo
import key_codes
import re
import string
import os
import sys

#----------------- class sgf_viewer ----------------#
class sgf_viewer(object):
	#------------- global variable ----------------#
	fp=None
	sgf_files=None
	last_game_index=None
	last_game_move=None
	x_inc = 18.7
	y_inc = 18.7
	y_min = 20
	x_min = 1
	current_seq = -1
	line_read = 0
	show_first_move=0
	stone_size=20
	# ellipse size, used to show last piece of stone
	e_offset=5
	e_size=stone_size/2+2
	# sequence = [ white/black, x_coor, y_coor, hide after this sequence]
	# ['w', 20, 60, 37] = white, x=20, y=60, hide after current_seq 37
	sequence = []
	file_path="c:\\Data\\python"
	player_w=u""
	player_w_rank=u""
	player_b=u""
	player_b_rank=u""
	game_result=u""
	komi=u""
	date=u""
	total_handicap=0
	total_move=0

	y_map = {'a':y_min,
			 'b':y_min+(y_inc*1),
			 'c':y_min+(y_inc*2),
			 'd':y_min+(y_inc*3),
			 'e':y_min+(y_inc*4),
			 'f':y_min+(y_inc*5),
			 'g':y_min+(y_inc*6),
			 'h':y_min+(y_inc*7),
			 'i':y_min+(y_inc*8),
			 'j':y_min+(y_inc*9),
			 'k':y_min+(y_inc*10),
			 'l':y_min+(y_inc*11),
			 'm':y_min+(y_inc*12),
			 'n':y_min+(y_inc*13),
			 'o':y_min+(y_inc*14),
			 'p':y_min+(y_inc*15),
			 'q':y_min+(y_inc*16),
			 'r':y_min+(y_inc*17),
			 's':y_min+(y_inc*18),
			 }
	x_map = {'a':x_min,
			 'b':x_min+(x_inc*1),
			 'c':x_min+(x_inc*2),
			 'd':x_min+(x_inc*3),
			 'e':x_min+(x_inc*4),
			 'f':x_min+(x_inc*5),
			 'g':x_min+(x_inc*6),
			 'h':x_min+(x_inc*7),
			 'i':x_min+(x_inc*8),
			 'j':x_min+(x_inc*9),
			 'k':x_min+(x_inc*10),
			 'l':x_min+(x_inc*11),
			 'm':x_min+(x_inc*12),
			 'n':x_min+(x_inc*13),
			 'o':x_min+(x_inc*14),
			 'p':x_min+(x_inc*15),
			 'q':x_min+(x_inc*16),
			 'r':x_min+(x_inc*17),
			 's':x_min+(x_inc*18),
			 }

	#----------------- __init__() ----------------#
	def __init__(self):
		self.main()

	#----------------- quit() ----------------#
	def quit():
		self.app_lock.signal()

	#----------------- press_select() ----------------#
	def press_select(self):
		if self.show_first_move:
			self.show_first_move=0
			self.current_seq = self.total_handicap-1;
		else:
			self.show_first_move=1
			self.current_seq = len(self.sequence)-1
		self.handle_redraw(())

	#----------------- press_down() ----------------#
	def press_down(self):
		self.current_seq -= 20
		if self.current_seq<self.total_handicap:
			self.current_seq=self.total_handicap-1
		self.handle_redraw(())

	#----------------- press_up() ----------------#
	def press_up(self):
		self.current_seq += 20
		if self.current_seq>len(self.sequence):
			self.current_seq=len(self.sequence)-1
		self.handle_redraw(())

	#----------------- press_right() ----------------#
	def press_right(self):
		self.current_seq += 1
		if self.current_seq>=len(self.sequence):
			#print ("i: total=%d, self.current_seq=%d" % (len(self.sequence), self.current_seq))
			self.current_seq=len(self.sequence)-1
		#print ("total=%d, self.current_seq=%d" % (len(self.sequence), self.current_seq))
		self.handle_redraw(())

	#----------------- press_left() ----------------#
	def press_left(self):
		self.current_seq -= 1
		if self.current_seq<self.total_handicap:
			self.current_seq=self.total_handicap-1
		self.handle_redraw(())

	def print_game_info(self):
		#self.img.text((15,15),u'List Text',(255,255,255))
		player_info=self.player_w +" ("+ self.player_w_rank +") vs "
		player_info=player_info+self.player_b + " ("+ self.player_b_rank +u")  "
		player_info=player_info +"["+ self.game_result +"] ; komi="+self.komi
		if self.total_handicap>0:
			player_info=player_info+" ; ha="+str(self.total_handicap)
		player_info=player_info+" ; date="+self.date
		self.img.text((5,12), player_info, fill=0xffffcc, font=("normal", 10, graphics.FONT_BOLD))
		#print appuifw.available_fonts()

		seq_info=u"current move = "+str(self.current_seq+1)+" of "+str(self.total_move)
		self.img.text((5, 390), seq_info, fill=0, font=("normal", 10, graphics.FONT_BOLD))

	#----------------- handle_redraw() ----------------#
	def handle_redraw(self, rect):
		count=0
		my_x=None
		self.img.blit(self.img_board, (0,0), (0,0))
		self.print_game_info()
		if self.current_seq>=0:
			#print self.current_seq
			#print self.sequence[count]
			## display the sequence from 0 to current_seq
			while count<=self.current_seq:
				my_x=None
				#print("count=%d, self.sequence=%c, %c", % (count, self.sequence[count][1], self.sequence[count][2]))
				if "]"==self.sequence[count][1]:
					count += 1
					continue
				if "W"==self.sequence[count][0]:
					my_x=self.x_map[self.sequence[count][1]]
					my_y=self.y_map[self.sequence[count][2]]
					self.img.blit(self.img_stone_w, target=(my_x, my_y), source=(0,0), mask=self.stoneMask)
				if "B"==self.sequence[count][0]:
					my_x=self.x_map[self.sequence[count][1]]
					my_y=self.y_map[self.sequence[count][2]]
					self.img.blit(self.img_stone_b, target=(my_x, my_y), source=(0,0), mask=self.stoneMask)
				count += 1
			if my_x:
				self.img.ellipse((my_x+self.e_offset, my_y+self.e_offset, my_x+self.e_size, my_y+self.e_size), 0xffffff, 0xffffff)
		self.canvas.blit(self.img)

	#----------------- init() ----------------#
	def init(self):
		self.current_seq = -1
		self.line_read = 0
		self.show_first_move=0
		self.total_handicap=0
		self.total_move=0
		del self.sequence[:]
		self.sequence=[]
		self.handle_redraw(())

	#----------------- parse_game_info() ----------------#
	def parse_game_info(self, game_info):
		#print game_info
		res=re.search(r"PW\[(.*?)\]", game_info, re.DOTALL)
		if res:
			self.player_w = u"%s" % res.group(1)
		res=re.search(r"PB\[(.*?)\]", game_info, re.DOTALL)
		if res:
			self.player_b = res.group(1)
		res=re.search(r"WR\[(.*?)\]", game_info, re.DOTALL)
		if res:
			self.player_w_rank = res.group(1)
		res=re.search(r"BR\[(.*?)\]", game_info, re.DOTALL)
		if res:
			self.player_b_rank = res.group(1)
		res=re.search(r"HA\[(.*?)\]", game_info, re.DOTALL)
		if res:
			self.total_handicap = string.atoi(res.group(1))
			#print("self.total_handicap=%d" % self.total_handicap)
			res=re.search(r"AB"+"\[(..)\]"*self.total_handicap, game_info, re.DOTALL)
			cnt=1
			while cnt<=self.total_handicap:
				self.sequence.append(('B',res.group(cnt)[0], res.group(cnt)[1], 0))
				cnt +=1
				self.current_seq=self.total_handicap-1
		res=re.search(r"RE\[(.*?)\]", game_info, re.DOTALL)
		if res:
			self.game_result = res.group(1)
		res=re.search(r"KM\[(.*?)\]", game_info, re.DOTALL)
		if res:
			self.komi=res.group(1)
		res=re.search(r"DT\[(.*?)\]", game_info, re.DOTALL)
		if res:
			self.date=res.group(1)

		print self.player_w
		print self.player_w_rank
		print self.player_b
		print self.player_b_rank
		print self.game_result
		print self.komi
		print self.total_handicap

	#----------------- read_sgf() ----------------#
	def read_sgf(self, f):
		# current rule works for kgs only...
		reg_seq=re.compile(r";(W|B)\[(.)(.)")
		lines=f.readlines()

		## find out the line the game play sequence started
		for i, line in enumerate(lines):
			result=reg_seq.match(line)
			if result:
				break

		## get game info
		game_info = "".join(lines[:i])
		self.parse_game_info(game_info);

		## get game played sequence
		for line in lines[i:]:
			result=reg_seq.match(line)
			if result:
				#print result.group()
				#print("%s move %s" % (result.group(1), result.group(2)))
				self.sequence.append((result.group(1), result.group(2), result.group(3)))
				#print self.sequence[:]
			self.total_move=len(self.sequence)

	#----------------- get_sgf_files() ----------------#
	def get_sgf_files(self):
		#files=[ f for f in os.listdir(self.file_path) if os.path.splitext(f)[1] is ".SGF"]
		files=map(unicode, os.listdir(self.file_path))
		if self.sgf_files:
			del self.sgf_files[:]
		self.sgf_files=[ f for f in files if os.path.splitext(f)[1].lower()==".sgf" ]
		#print self.sgf_files

	#----------------- open_file() ----------------#
	def open_file(self):
		print "open_file"
		self.get_sgf_files()
		index=appuifw.selection_list(self.sgf_files)
		if index!=None:
			print self.sgf_files[index]
			print self.file_path+"\\"+self.sgf_files[index]
			self.init()
			f=open(self.file_path+"\\"+self.sgf_files[index])
			self.read_sgf(f)
			self.handle_redraw(())
			#print self.sequence[:]

	#----------------- change_path() ----------------#
	def change_path(self):
		print "change_path"
		cur_dir=self.file_path
		index =-1
		while index!=0 and index!=None:
			#print "inwhile: cur_dir=%s" % cur_dir
			dir=[ name for name in os.listdir(cur_dir) if os.path.isdir(os.path.join(cur_dir, name)) ]
			# insert ".." to go up to root directory
			dir.insert(0, "..")
			# done selection
			dir.insert(0, "done[%s]" % cur_dir)
			mydir=map(unicode, dir)
			#print dir[:]
			index=appuifw.selection_list(mydir)
			if index:
				cur_dir=os.path.join(cur_dir, mydir[index])
				self.file_path=cur_dir
				self.get_sgf_files()
				#print "cur_dir=%s" % (cur_dir)
		#if index==0:
		#	self.file_path=cur_dir
			#print "self.file_path=%s" % self.file_path

	#----------------- read_file_info() ----------------#
	def read_file_info(self, fp):
		re_path=re.compile("file_path=(.*)")
		re_last_game_index=re.compile("last_game_index=(.*)")
		re_last_game_move=re.compile("last_game_move=(.*)")
		#func_ptr={0:lambda x: setattr(file_path, , 1:set_game_index, 2:set_game_move}
		#for i, line in enumerate(fp):
		#	res=re_path.match(info[0])
		#if res:
		#	switch(i):
		#	file_info_data.append(res.group(1))

		#if file_info_data[0]
		#res=re_last_game_index.match(info[1])
		#if res:
		#	self.last_game_index=res.group(1)
		#res=re_last_game_move.match(info[2])
		#if res:
		#	my_game=file_path+"\\"+sgf_files[self.last_game_index]
		#	if os.path.isfile(my_game):
		#		f = open()
		#		read_sgf(f)
		#		self.current_seq=res.group(1)
		#	else:
		#		print "my_game is not file=%s" % my_game

	#----------------- exit_app() ----------------#
	def exit_app(self):
		if self.fp:
			self.fp.seek(0)
			self.fp.write("file_path=%s" % self.file_path)
			if self.last_game_index:
				self.fp.write("last_game_index=%d" % self.last_game_index)
				self.fp.write("last_game_move=%d" % self.last_game_move)
			self.fp.close()
		self.app_lock.signal()

	#----------------- main() ----------------#
	def main(self):
		## load image
		#(width, height) = sysinfo.display_pixels()
		#self.img=graphics.Image.new((width,height))
		#print("size is %d %d" %(width, height))

		## as a convenient way to switch between c:\\(pc) or e:\\(hp)
		self.img_board_path=self.file_path+"\\board.jpg"
		if not os.path.isfile(self.img_board_path):
			self.file_path="e:\\Data\\python"

		self.file_info=self.file_path+"\\file.info"
		fp=open(self.file_info, "r+")
		if fp==None:
			print "file %s open error" % self.file_info
			sys.exit(2)
		self.get_sgf_files()
		self.read_file_info(fp)

		self.img=graphics.Image.new((360,640))
		self.img_board=graphics.Image.open(self.file_path+"\\board.jpg")
		# mask is 8-bit grey scale (L) or 1 (1-bit)
		self.stoneMask = graphics.Image.new(size = (self.stone_size,self.stone_size),mode = 'L')
		self.stoneMask.load(self.file_path+"\\stone_mask.jpg")
		self.img_stone_w=graphics.Image.open(self.file_path+"\\stone_w.jpg")
		self.img_stone_b=graphics.Image.open(self.file_path+"\\stone_b.jpg")

		## hide the virtual directional pad
		#appuifw.app.directional_pad=False;
		self.canvas=appuifw.Canvas(event_callback=None, redraw_callback=self.handle_redraw)
		#appuifw.app.title=unicode(self.player_w +'('+self.player_w_rank+')'+' vs '+ self.player_b+'('+self.player_b_rank+')')
		#appuifw.app.title=u"hahaha"
		appuifw.app.body=self.canvas
		appuifw.app.exit_key_handler=quit
		appuifw.app.screen='large'
		appuifw.app.menu = [(u"Exit", self.exit_app), (u"Open SGF File", self.open_file), (u"Change Path", self.change_path)]
		self.canvas.bind(key_codes.EKeySelect, self.press_select)
		self.canvas.bind(key_codes.EKeyDownArrow, self.press_down)
		self.canvas.bind(key_codes.EKeyUpArrow, self.press_up)
		self.canvas.bind(key_codes.EKeyRightArrow, self.press_right)
		self.canvas.bind(key_codes.EKeyLeftArrow, self.press_left)

		self.init()

		# read sgf file
		#f = open(self.file_path+"\\game1.sgf")
		#read_sgf(f)
		#draw list item text
		#self.img.text((30,30),u'List Text',(0,0,0),"title")

		self.app_lock=e32.Ao_lock()
		self.app_lock.wait()

#----------------- start_app ----------------#
my_sgf_viewer=sgf_viewer()
