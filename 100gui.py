import appuifw, e32, graphics, e32dbm
import sysinfo
import key_codes
import re
import string
import os
import sys
from xml.dom import minidom

#----------------- class sgf_viewer ----------------#
class sgf_viewer(object):
	#------------- [ global variable ]----------------#
	main_path=u"c:\\Data\\python"
	sgf_file_path=u"c:\\Data\\python"
	xmldoc = None
	xml_last_game = None
	xml_history = None
	xml_history_last_idx = None
	xml_file = main_path+"\\go_viewer.xml"
	dbm=None
	sgf_files=None
	last_game_index=None
	last_game_move=None
	fp_debug=None
	on_debug=True
	open_last_game=True
	x_inc = 18.7
	y_inc = 18.7
	y_min = 20
	x_min = 1
	cur_seq = -1
	line_read = 0
	show_first_move=0
	stone_size=20
	# ellipse size, used to show last piece of stone
	e_offset=5
	e_size=stone_size/2+2
	# sequence = [ white/black, x_coor, y_coor, hide after this sequence]
	# ['w', 20, 60, 37] = white, x=20, y=60, hide after cur_seq 37
	sequence = []
	player_w=u""
	player_w_rank=u""
	player_b=u""
	player_b_rank=u""
	game_result=u""
	komi=u""
	date=u""
	total_handicap=0
	total_move=0
	img=None

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

	total_his = 5
	no_game="0"
	## we keep the history of last 5 game, in round-robin (fifo)
	## todo: add/remove favourite game
	xml_init = ('''<?xml version="1.0" ?>
	<data>
	<last_game>%s</last_game>
	<history>0,0,0,0,0</history>
	<his_last_idx>%d</his_last_idx>
	</data>
	''' % (no_game, total_his))

	#----------------- __init__() ----------------#
	def __init__(self):
		self.main()

	#----------------- quit() ----------------#
	def quit():
		self.app_lock.signal()

	#----------------- debug() ----------------#
	def dbg(self, str, *args):
		if self.on_debug:
			#print (str % args)
			self.fp_debug.write((str+'\n') % args)
			print (str % args)

	#----------------- press_select() ----------------#
	def press_select(self):
		if self.show_first_move:
			self.show_first_move=0
			self.cur_seq = self.total_handicap-1;
		else:
			self.show_first_move=1
			self.cur_seq = len(self.sequence)-1
		self.handle_redraw(())

	#----------------- press_down() ----------------#
	def press_down(self):
		self.cur_seq -= 20
		if self.cur_seq<self.total_handicap:
			self.cur_seq=self.total_handicap-1
		self.handle_redraw(())

	#----------------- press_up() ----------------#
	def press_up(self):
		self.cur_seq += 20
		if self.cur_seq>len(self.sequence):
			self.cur_seq=len(self.sequence)-1
		self.handle_redraw(())

	#----------------- press_right() ----------------#
	def press_right(self):
		self.cur_seq += 1
		if self.cur_seq>=len(self.sequence):
			self.cur_seq=len(self.sequence)-1
		self.handle_redraw(())

	#----------------- press_left() ----------------#
	def press_left(self):
		self.cur_seq -= 1
		if self.cur_seq<self.total_handicap:
			self.cur_seq=self.total_handicap-1
		self.handle_redraw(())

	def print_game_info(self):
		#self.img.text((15,15),u'List Text',(255,255,255))
		player_info=self.player_w +" ("+ self.player_w_rank +") vs "
		player_info=player_info+self.player_b+" ("+ self.player_b_rank +u")  "
		player_info=player_info +"["+ self.game_result +"] ; komi="+self.komi
		if self.total_handicap>0:
			player_info=player_info+" ; ha="+str(self.total_handicap)
		player_info=player_info+" ; date="+self.date
		self.img.text((5,12), player_info, fill=0xffffcc,
							font=("normal", 10, graphics.FONT_BOLD))
		#print appuifw.available_fonts()

		seq_info=u"current move = "+str(self.cur_seq+1)+" of "
		seq_info+=str(self.total_move)
		self.img.text((5, 390), seq_info, fill=0,
						font=("normal", 10, graphics.FONT_BOLD))

	#----------------- handle_redraw() ----------------#
	def handle_redraw(self, rect):
		count=0
		my_x=None
		self.img.blit(self.img_board, (0,0), (0,0))
		self.print_game_info()
		if self.sequence and self.cur_seq>=0:
			#self.dbg("handle_redraw: cur_seq=%s", self.cur_seq)
			#self.dbg("sequence=%s", self.sequence[:])
			## display the sequence from 0 to cur_seq
			while count<=self.cur_seq:
				my_x=None
				#print "handle_redraw, count=", count
				if "]"==self.sequence[count][1]:
					count += 1
					continue
				if "W"==self.sequence[count][0]:
					my_x=self.x_map[self.sequence[count][1]]
					my_y=self.y_map[self.sequence[count][2]]
					self.img.blit(self.img_stone_w, target=(my_x, my_y),
											source=(0,0), mask=self.stoneMask)
				if "B"==self.sequence[count][0]:
					my_x=self.x_map[self.sequence[count][1]]
					my_y=self.y_map[self.sequence[count][2]]
					self.img.blit(self.img_stone_b, target=(my_x, my_y),
											source=(0,0), mask=self.stoneMask)
				count += 1
			if my_x:
				self.img.ellipse((my_x+self.e_offset, my_y+self.e_offset,
					my_x+self.e_size, my_y+self.e_size), 0xffffff, 0xffffff)
		self.canvas.blit(self.img)

	#----------------- init() ----------------#
	def init(self):
		self.cur_seq = -1
		#self.dbg("last_game_move=%s" % self.last_game_move)
		#self.dbg("cur_seq=%s" % self.cur_seq)
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
			res=re.search(r"AB"+"\[(..)\]"*self.total_handicap,
							game_info, re.DOTALL)
			cnt=1
			while cnt<=self.total_handicap:
				self.sequence.append(('B',res.group(cnt)[0],
										res.group(cnt)[1], 0))
				cnt +=1
			if self.open_last_game and self.last_game_move:
				## open last game
				self.cur_seq = self.last_game_move
			else:
				self.cur_seq=self.total_handicap-1
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
			res=reg_seq.match(line)
			if res:
				#print res.group()
				#print("%s move %s" % (res.group(1), res.group(2)))
				self.sequence.append((res.group(1),res.group(2),res.group(3)))
				#print self.sequence[:]
			self.total_move=len(self.sequence)

	#----------------- get_sgf_files() ----------------#
	def get_sgf_files(self):
		files=map(unicode, os.listdir(self.sgf_file_path))
		if self.sgf_files:
			del self.sgf_files[:]
		self.sgf_files=[ f for f in files if \
							os.path.splitext(f)[1].lower()==".sgf" ]
		#print self.sgf_files

	#----------------- process_file() ----------------#
	def process_file(self, index):
		#self.dbg(self.sgf_files[index])
		#self.dbg(self.sgf_file_path+"\\"+self.sgf_files[index])
		self.init()
		game_file = self.sgf_file_path+"\\"+self.sgf_files[index]
		f=open(game_file)
		self.xml_last_game.data = game_file
		self.read_sgf(f)
		self.handle_redraw(())
		self.last_game_index=index
		#print self.sequence[:]

	#----------------- open_game() ----------------#
	def open_game(self):
		print "open_game"
		self.get_sgf_files()
		index=appuifw.selection_list(self.sgf_files)
		if index!=None:
			self.process_file(index)

	#----------------- change_path() ----------------#
	def change_path(self):
		print "change_path"
		cur_dir=self.sgf_file_path
		index =-1
		while index!=0 and index!=None:
			#print "inwhile: cur_dir=%s" % cur_dir
			dir=[ name for name in os.listdir(cur_dir) if \
					os.path.isdir(os.path.join(cur_dir, name)) ]
			# insert ".." to go up to root directory
			dir.insert(0, "..")
			# done selection
			dir.insert(0, "done[%s]" % cur_dir)
			mydir=map(unicode, dir)
			#print dir[:]
			index=appuifw.selection_list(mydir)
			if index:
				cur_dir=os.path.join(cur_dir, mydir[index])
				self.sgf_file_path=cur_dir
				self.get_sgf_files()
				#print "cur_dir=%s" % (cur_dir)
		#if index==0:
		#	self.file_path=cur_dir
			#print "self.file_path=%s" % self.file_path

	#----------------- set_dbm_prop() ----------------#
	def set_dbm_prop(self, key, value):
		if str(value) == value:
			## if it is string, cast to unicode
			value = "u\"%s\"" % value
			self.dbm[key] = value
		else:
			self.dbm[key] = str(value)

	#----------------- get_dbm_prop() ----------------#
	def get_dbm_prop(self, key):
		try:
			return eval(self.dbm[key])
		except:
			## item not exit yet, return none
			return None

	#----------------- get_last_game_idx() ----------------#
	def get_last_game_idx(self):
		path = os.path.dirname(self.xml_last_game.data)
		if os.path.isdir(path):
			self.sgf_file_path = path
			self.get_sgf_files()
			basename = os.path.basename(self.xml_last_game.data)
			for i, line in enumerate(self.sgf_files):
				#self.dbg("line=%s, basename=%s", line, basename)
				if basename == line:
					#self.dbg("basename==line, i=%d", i)
					self.last_game_index = i
					break
		else:
			self.dbg("self.xml_last_game (%s) does not have valid"
					"path", self.xml_last_game)

	#----------------- read_last_opened_game() ----------------#
	def read_last_opened_game(self):
		#temp=self.get_dbm_prop('sgf_file_path')
		#if temp:
		#	self.sgf_file_path=temp
		#self.last_game_index=self.get_dbm_prop('last_game_index')
		#self.last_game_move=self.get_dbm_prop('last_game_move')
		self.get_last_game_idx()
		self.last_game_move=self.get_dbm_prop('last_game_move')
		self.dbg("last game index=%s" % self.last_game_index)
		if self.last_game_index!=None:
			## if last opened game found
			self.get_sgf_files()
			self.process_file(self.last_game_index)

	#----------------- next_game() ----------------#
	def next_game(self):
		if self.last_game_index:
			temp=self.last_game_index+1
			if temp >= len(sgf_files):
				print "loop back to first game"
				temp = 0
			next_sgf=self.sgf_file_path+"\\"+self.sgf_files[temp]
			self.dbg("next_sgf = %s" % next_sgf)
			if os.path.isfile(next_sgf):
				self.process_file(temp)
				## assign new value to last_game_index
				self.last_game_index=temp
		else:
			print "last_game_index not valid", self.last_game_index

	#----------------- exit_app() ----------------#
	def exit_app(self):
		#self.dbg("sgf_file_path=%s" % self.sgf_file_path)
		#self.dbg("last_game_index=%d" % self.last_game_index)
		#self.dbg("outside")
		#if self.dbm:
		#	self.dbg("inside")
		#	#self.dbm.close()
		#	## delete the exisitng file by creating a new one
		#	#self.dbm=e32dbm.open(self.last_opened_game, "n")
		#	#self.set_dbm_prop('sgf_file_path', self.sgf_file_path)
		#	#self.set_dbm_prop('last_game_index', self.last_game_index)
		#	#self.set_dbm_prop('last_game_move', self.cur_seq)
		#	#self.dbm['sgf_file_path2'] =u"haha"
		#	self.dbm.close()

		## write the xml file
		xml_fp = open(self.xml_file, "w")
		xml_fp.write('%s' % self.xmldoc.toxml())
		xml_fp.close()

		if self.on_debug:
			self.fp_debug.close()
		self.app_lock.signal()

	#----------------- main() ----------------#
	def main(self):
		## load image
		#(width, height) = sysinfo.display_pixels()
		#self.img=graphics.Image.new((width,height))
		#print("size is %d %d" %(width, height))

		## file for debug use
		if self.on_debug:
			self.fp_debug = open(self.main_path+'\\debug.txt', 'w+')

		## as a convenient way to switch between c:\\(pc) or e:\\(hp)
		self.img_board_path=self.main_path+"\\board.jpg"
		if not os.path.isfile(self.img_board_path):
			self.main_path="e:\\Data\\python"

		## check if the xml data file exist, create if non-existence
		if not os.path.isfile(self.xml_file):
			xml_fp = open(self.xml_file, "w")
			xml_fp.write('%s' % self.xml_init)
			xml_fp.close()
			self.dbg('writting to xml_file')
		self.xmldoc = minidom.parse(self.xml_file)
		self.xml_last_game = self.xmldoc.getElementsByTagName('last_game')[0].childNodes[0]
		#self.dbg("kn = %s ", dir(self.xml_last_game))
		#self.dbg("kn2 = %s ", self.xml_last_game.__dict__)
		#self.dbg("kn2 = %s ", self.xml_last_game.data)

		#self.last_opened_game=self.main_path+"\\last_opened_game"
		#try:
		#	self.dbm=e32dbm.open(self.last_opened_game, "w")
		#except:
		#	# assume file not exist, create new
		#	self.dbm=e32dbm.open(self.last_opened_game, "n");
		#if self.dbm==None:
		#	print "file %s open error" % self.last_opened_game
		#	sys.exit(2)
		#self.read_last_opened_game()

		self.img=graphics.Image.new((360,640))
		self.img_board=graphics.Image.open(self.main_path+"\\board.jpg")
		# mask is 8-bit grey scale (L) or 1 (1-bit)
		self.stoneMask = graphics.Image.new(size = \
							(self.stone_size,self.stone_size),mode = 'L')
		self.stoneMask.load(self.main_path+"\\stone_mask.jpg")
		self.img_stone_w=graphics.Image.open(self.main_path+"\\stone_w.jpg")
		self.img_stone_b=graphics.Image.open(self.main_path+"\\stone_b.jpg")

		## hide the virtual directional pad
		#appuifw.app.directional_pad=False;
		self.canvas=appuifw.Canvas(event_callback=None,
							redraw_callback=self.handle_redraw)
		#appuifw.app.title=unicode(self.player_w +'('+self.player_w_rank+')'+\
							#' vs '+ self.player_b+'('+self.player_b_rank+')')
		appuifw.app.body=self.canvas
		appuifw.app.exit_key_handler=self.exit_app
		appuifw.app.screen='large'
		appuifw.app.menu = [(u"Exit", self.exit_app), (u"Open SGF File", \
						self.open_game), (u"Change Path", self.change_path),
						(u"Goto Next Game", self.next_game)]
		self.canvas.bind(key_codes.EKeySelect, self.press_select)
		self.canvas.bind(key_codes.EKeyDownArrow, self.press_down)
		self.canvas.bind(key_codes.EKeyUpArrow, self.press_up)
		self.canvas.bind(key_codes.EKeyRightArrow, self.press_right)
		self.canvas.bind(key_codes.EKeyLeftArrow, self.press_left)

		self.app_lock=e32.Ao_lock()

		## get last game info if exists
		if self.xml_last_game.data != self.no_game:
			self.dbg("self.xml_last_game.data=%s", self.xml_last_game.data)
			self.read_last_opened_game()
		else:
			self.dbg("no last game read")

		self.open_last_game=False
		self.app_lock.wait()

#----------------- start_app ----------------#
my_sgf_viewer=sgf_viewer()
