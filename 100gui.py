import appuifw, e32, graphics
import sysinfo
import key_codes
import re
import string

#----------------- global variable ----------------#
x_inc = 18.7
y_inc = 18.7
y_min = 20
x_min = 1
current_seq = -1
#current_seq = 30
sequence = []
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

#----------------- function() ----------------#
def quit():
	app_lock.signal()

def press_select():
	print "select"

def press_down():
	global y_inc
	global y_coor
	y_coor += y_inc
	handle_redraw(())

def press_up():
	global y_inc
	global y_coor
	y_coor -= y_inc
	handle_redraw(())

def press_right():
	global x_coor
	global x_inc
	global current_seq
	current_seq += 1
	if current_seq>max(sequence)[0]:
		current_seq=max(sequence)
	x_coor += x_inc
	handle_redraw(())

def press_left():
	global x_coor
	global x_inc
	global current_seq
	current_seq -= 1
	if current_seq<0:
		current_seq=0
	x_coor -= x_inc
	handle_redraw(())

def handle_redraw(rect):
	global current_seq
	count=0
	img.blit(img_board, (0,0), (0,0))
	#img.blit(img_stone_w, target=(x_coor, y_coor), source=(0,0), mask=stoneMask)
	#img.blit(img_stone_b, target=(20, 40), source=(0,0), mask=stoneMask)
	#img.blit(img_stone_w, target=(20, 60), source=(0,0), mask=stoneMask)

	#img.text((60,60),u'List Text',(0,0,0),"normal")

	#img.blit(img_stone_b, target=(40, 20), source=(0,0), mask=stoneMask)

	if current_seq>=0:
		print sequence[count]
		#print ("%d, %d" %(sequence[count][0], sequence[count][1]))
		## display the sequence from 0 to current_seq
		while count<=current_seq:
			if "W"==sequence[count][0]:
				img.blit(img_stone_w, target=(x_map[sequence[count][1]], y_map[sequence[count][2]]), source=(0,0), mask=stoneMask)
			if "B"==sequence[count][0]:
				img.blit(img_stone_b, target=(x_map[sequence[count][1]], y_map[sequence[count][2]]), source=(0,0), mask=stoneMask)
			count += 1
	canvas.blit(img)

def read_sgf(f):
	# current rule works for kgs only...
	global sequence
	global current_seq
	player_w=""
	player_w_rank=""
	player_b=""
	player_b_rank=""
	total_handicap=0
	komi=""
	rules=""
	result=""
	reg_seq=re.compile(r";(W|B)\[(.)(.)")
	lines=f.readlines()

	## find out the line the game play sequence started
	for i, line in enumerate(lines):
		result=reg_seq.match(line)
		if result:
			break

	## get game info
	game_info = "".join(lines[:i])
	#print game_info
	res=re.search(r"PW\[(.*?)\]", game_info, re.DOTALL)
	if res:
		player_w = res.group(1)
	res=re.search(r"PB\[(.*?)\]", game_info, re.DOTALL)
	if res:
		player_b = res.group(1)
	res=re.search(r"WR\[(.*?)\]", game_info, re.DOTALL)
	if res:
		player_w_rank = res.group(1)
	res=re.search(r"BR\[(.*?)\]", game_info, re.DOTALL)
	if res:
		player_b_rank = res.group(1)
	res=re.search(r"HA\[(.*?)\]", game_info, re.DOTALL)
	if res:
		total_handicap = string.atoi(res.group(1))
		res=re.search(r"AB"+"\[(..)\]"*total_handicap, game_info, re.DOTALL)
		cnt=1
		while cnt<=total_handicap:
			sequence.append(res.group(cnt))
			cnt +=1

	#print player_w
	#print player_b
	#print player_w_rank
	#print player_b_rank
	#print total_handicap
	#print sequence

	#for line in lines[0:i]:
	#	if player_w=="":
	#		#print line
	#		result=re.match(r"PW\[(.*?)\]",line)
	#		if result:
	#			player_w=result.group(1)
	#			print player_w

	## get game played sequence
	#for line in lines[i:]:
	#	result=reg_seq.match(line)
	#	if result:
	#		#print result.group()
	#		#print("%s move %s" % (result.group(1), result.group(2)))
	#		sequence.append((result.group(1), result.group(2), result.group(3)))
	#		#print sequence[:]

#----------------- main() ----------------#
## load image
#(width, height) = sysinfo.display_pixels()
#img=graphics.Image.new((width,height))
#print("size is %d %d" %(width, height))
img=graphics.Image.new((360,640))
img_board=graphics.Image.open("c:\\Data\\python\\board.jpg")
# mask is 8-bit grey scale (L) or 1 (1-bit)
stoneMask = graphics.Image.new(size = (20,20),mode = 'L')
stoneMask.load("c:\\Data\\python\\stone_mask.jpg")
img_stone_w=graphics.Image.open("c:\\Data\\python\\stone_w.jpg")
img_stone_b=graphics.Image.open("c:\\Data\\python\\stone_b.jpg")

# read sgf file
f = open("c:\\Data\\python\\game1.sgf")
read_sgf(f)
#draw list item text
#img.text((30,30),u'List Text',(0,0,0),"title")

## hide the virtual directional pad
#appuifw.app.directional_pad=False;
canvas=appuifw.Canvas(event_callback=None, redraw_callback=handle_redraw)
#appuifw.app.title=unicode(player_w +'('+player_w_rank+')'+' vs '+ player_b+'('+player_b_rank+')')
#appuifw.app.title=u"hahaha"
appuifw.app.body=canvas
appuifw.app.exit_key_handler=quit
appuifw.app.screen='large'
canvas.bind(key_codes.EKeySelect, press_select)
canvas.bind(key_codes.EKeyDownArrow, press_down)
canvas.bind(key_codes.EKeyUpArrow, press_up)
canvas.bind(key_codes.EKeyRightArrow, press_right)
canvas.bind(key_codes.EKeyLeftArrow, press_left)

app_lock=e32.Ao_lock()
app_lock.wait()


