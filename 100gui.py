import appuifw, e32, graphics
import sysinfo

#Define the exit function
def quit():app_lock.signal()
appuifw.app.exit_key_handler=quit
appuifw.app.screen='large'
selectedindex=0

def handle_redraw(rect):
     canvas.blit(img)

def selected_index():
    return selectedindex

#(width, height) = sysinfo.display_pixels()
img=graphics.Image.new((360,640))
#img=graphics.Image.new((width,height))
#print("size is %d %d" %(width, height))

img_board=graphics.Image.open("c:\\Data\\python\\board.jpg")
img_stone_w=graphics.Image.open("c:\\Data\\python\\box.jpg")
#img2=graphics.Image.open("e:\\Images\\area.png")

#draw list item background
img.blit(img_board, (0,0), (0,0))
#draw list item text
img.text((30,30),u'List Text',(0,0,0),"title")

# hide the virtual directional pad
appuifw.app.directional_pad=False;
canvas=appuifw.Canvas(event_callback=None, redraw_callback=handle_redraw)
appuifw.app.body=canvas

app_lock=e32.Ao_lock()
app_lock.wait()


