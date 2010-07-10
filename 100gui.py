import appuifw, e32, graphics
import sysinfo
import key_codes
import re
import string
import os

#----------------- global variable ----------------#
x_inc = 18.7
y_inc = 18.7
y_min = 20
x_min = 1
current_seq = -1
total_handicap = 0
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
x_coor=x_map['s']
y_coor=y_map['s']

#----------------- quit() ----------------#
def quit():
	app_lock.signal()

#----------------- press_select() ----------------#
def press_select():
	global show_first_move
	global current_seq
	global sequence
	global total_handicap
	if show_first_move:
		show_first_move=0
		current_seq = total_handicap-1;
	else:
		show_first_move=1
		current_seq = len(sequence)-1
	handle_redraw(())

#----------------- press_down() ----------------#
def press_down():
	global y_inc
	global y_coor
	global current_seq
	current_seq -= 20
	if current_seq<total_handicap:
		current_seq=total_handicap-1
	y_coor += y_inc
	handle_redraw(())

#----------------- press_up() ----------------#
def press_up():
	global y_inc
	global y_coor
	global current_seq
	current_seq += 20
	if current_seq>len(sequence):
		current_seq=len(sequence)-1
	y_coor -= y_inc
	handle_redraw(())

#----------------- press_right() ----------------#
def press_right():
	global x_coor
	global x_inc
	global current_seq
	current_seq += 1
	if current_seq>=len(sequence):
		#print ("i: total=%d, current_seq=%d" % (len(sequence), current_seq))
		current_seq=len(sequence)-1
	#print ("total=%d, current_seq=%d" % (len(sequence), current_seq))
	x_coor += x_inc
	handle_redraw(())

#----------------- press_left() ----------------#
def press_left():
	global x_coor
	global x_inc
	global current_seq
	current_seq -= 1
	if current_seq<total_handicap:
		current_seq=total_handicap-1
	x_coor -= x_inc
	handle_redraw(())

#----------------- handle_redraw() ----------------#
def handle_redraw(rect):
	global current_seq
	count=0
	my_x=None
	img.blit(img_board, (0,0), (0,0))
	#img.blit(img_stone_w, target=(x_coor, y_coor), source=(0,0), mask=stoneMask)
	if current_seq>=0:
		#print current_seq
		#print sequence[count]
		## display the sequence from 0 to current_seq
		while count<=current_seq:
			my_x=None
			#print("count=%d, sequence=%c, %c", % (count, sequence[count][1], sequence[count][2]))
			if "]"==sequence[count][1]:
				count += 1
				continue
			if "W"==sequence[count][0]:
				my_x=x_map[sequence[count][1]]
				my_y=y_map[sequence[count][2]]
				img.blit(img_stone_w, target=(my_x, my_y), source=(0,0), mask=stoneMask)
			if "B"==sequence[count][0]:
				my_x=x_map[sequence[count][1]]
				my_y=y_map[sequence[count][2]]
				img.blit(img_stone_b, target=(my_x, my_y), source=(0,0), mask=stoneMask)
			count += 1
		if my_x:
			img.ellipse((my_x+e_offset, my_y+e_offset, my_x+e_size, my_y+e_size), 0xffffff, 0xffffff)
	canvas.blit(img)

#----------------- init() ----------------#
def init():
	global current_seq
	global total_handicap
	global line_read
	global show_first_move
	global sequence
	current_seq = -1
	line_read = 0
	show_first_move=0
	total_handicap=0
	del sequence[:]
	sequence=[]
	handle_redraw(())

#----------------- parse_game_info() ----------------#
def parse_game_info(game_info):
	global sequence
	global current_seq
	global total_handicap
	#print game_info
	res=re.search(r"PW\[(.*?)\]", game_info, re.DOTALL)
	if res:
		player_w = res.group(1)
		print player_w
	res=re.search(r"PB\[(.*?)\]", game_info, re.DOTALL)
	if res:
		player_b = res.group(1)
		print player_b
	res=re.search(r"WR\[(.*?)\]", game_info, re.DOTALL)
	if res:
		player_w_rank = res.group(1)
	res=re.search(r"BR\[(.*?)\]", game_info, re.DOTALL)
	if res:
		player_b_rank = res.group(1)
	res=re.search(r"HA\[(.*?)\]", game_info, re.DOTALL)
	if res:
		total_handicap = string.atoi(res.group(1))
		#print("total_handicap=%d" % total_handicap)
		res=re.search(r"AB"+"\[(..)\]"*total_handicap, game_info, re.DOTALL)
		cnt=1
		while cnt<=total_handicap:
			sequence.append(('B',res.group(cnt)[0], res.group(cnt)[1], 0))
			cnt +=1
			current_seq=total_handicap-1

	#print player_w_rank
	#print player_b_rank
	#print total_handicap
	#print sequence
	#print ("current_seq=%d" % current_seq)

#----------------- read_sgf() ----------------#
def read_sgf(f):
	# current rule works for kgs only...
	global sequence
	reg_seq=re.compile(r";(W|B)\[(.)(.)")
	lines=f.readlines()

	## find out the line the game play sequence started
	for i, line in enumerate(lines):
		result=reg_seq.match(line)
		if result:
			break

	## get game info
	game_info = "".join(lines[:i])
	parse_game_info(game_info);

	## get game played sequence
	for line in lines[i:]:
		result=reg_seq.match(line)
		if result:
			#print result.group()
			#print("%s move %s" % (result.group(1), result.group(2)))
			sequence.append((result.group(1), result.group(2), result.group(3)))
			#print sequence[:]

#----------------- open_file() ----------------#
def open_file():
	print "open_file"
	#files=[ f for f in os.listdir(file_path) if os.path.splitext(f)[1] is ".SGF"]
	files=map(unicode, os.listdir(file_path))
	sgf_files=[ f for f in files if os.path.splitext(f)[1].lower()==".sgf" ]
	#print sgf_files
	index=appuifw.selection_list(sgf_files)
	if index!=None:
		print sgf_files[index]
		print file_path+"\\"+sgf_files[index]
		init()
		f=open(file_path+"\\"+sgf_files[index])
		read_sgf(f)
		handle_redraw(())
		#print sequence[:]
	print "open %d " % index

#----------------- change_path() ----------------#
def change_path():
	global file_path
	print "change_path"
	cur_dir=file_path
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
			#print "cur_dir=%s" % (cur_dir)
	if index==0:
		file_path=cur_dir
		#print "file_path=%s" % file_path

#----------------- main() ----------------#
## load image
#(width, height) = sysinfo.display_pixels()
#img=graphics.Image.new((width,height))
#print("size is %d %d" %(width, height))
img=graphics.Image.new((360,640))
img_board=graphics.Image.open(file_path+"\\board.jpg")
# mask is 8-bit grey scale (L) or 1 (1-bit)
stoneMask = graphics.Image.new(size = (stone_size,stone_size),mode = 'L')
stoneMask.load(file_path+"\\stone_mask.jpg")
img_stone_w=graphics.Image.open(file_path+"\\stone_w.jpg")
img_stone_b=graphics.Image.open(file_path+"\\stone_b.jpg")

## hide the virtual directional pad
#appuifw.app.directional_pad=False;
canvas=appuifw.Canvas(event_callback=None, redraw_callback=handle_redraw)
#appuifw.app.title=unicode(player_w +'('+player_w_rank+')'+' vs '+ player_b+'('+player_b_rank+')')
#appuifw.app.title=u"hahaha"
appuifw.app.body=canvas
appuifw.app.exit_key_handler=quit
appuifw.app.screen='large'
appuifw.app.menu = [(u"Open SGF File", open_file), (u"Change Path", change_path)]
canvas.bind(key_codes.EKeySelect, press_select)
canvas.bind(key_codes.EKeyDownArrow, press_down)
canvas.bind(key_codes.EKeyUpArrow, press_up)
canvas.bind(key_codes.EKeyRightArrow, press_right)
canvas.bind(key_codes.EKeyLeftArrow, press_left)

init()

# read sgf file
f = open("c:\\Data\\python\\game1.sgf")
read_sgf(f)
#draw list item text
#img.text((30,30),u'List Text',(0,0,0),"title")

app_lock=e32.Ao_lock()
app_lock.wait()

