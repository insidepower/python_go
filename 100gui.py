import appuifw, e32, graphics
import sysinfo
import key_codes

#----------------- global variable ----------------#
x_coor=20
y_coor=20
x_inc = 18.7
y_inc = 18.7

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
	x_coor += x_inc
	handle_redraw(())

def press_left():
	global x_coor
	global x_inc
	x_coor -= x_inc
	handle_redraw(())

def handle_redraw(rect):
	img.blit(img_board, (0,0), (0,0))
	img.blit(img_stone_w, target=(x_coor,y_coor), source=(0,0), mask=stoneMask)
	img.blit(img_stone_b, target=(20, 40), source=(0,0), mask=stoneMask)
	img.blit(img_stone_w, target=(20, 60), source=(0,0), mask=stoneMask)

	#img.blit(img_stone_b, target=(40, 20), source=(0,0), mask=stoneMask)
	canvas.blit(img)

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

#draw list item text
#img.text((30,30),u'List Text',(0,0,0),"title")

## hide the virtual directional pad
#appuifw.app.directional_pad=False;
canvas=appuifw.Canvas(event_callback=None, redraw_callback=handle_redraw)
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


