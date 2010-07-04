import appuifw, e32, graphics
import sysinfo

#Define the exit function
def quit():app_lock.signal()
appuifw.app.exit_key_handler=quit
appuifw.app.screen='large'
x_coor=20
y_coor=20

def handle_redraw(rect):
     canvas.blit(img)

#(width, height) = sysinfo.display_pixels()
img=graphics.Image.new((360,640))
#img=graphics.Image.new((width,height))
#print("size is %d %d" %(width, height))

img_board=graphics.Image.open("c:\\Data\\python\\board.jpg")
# mask is 8-bit grey scale (L) or 1 (1-bit)
stoneMask = graphics.Image.new(size = (20,21),mode = 'L')
stoneMask.load("c:\\Data\\python\\stone_mask.jpg")
img_stone_w=graphics.Image.open("c:\\Data\\python\\stone_w.jpg")
img_stone_b=graphics.Image.open("c:\\Data\\python\\stone_b.jpg")
#img2=graphics.Image.open("e:\\Images\\area.png")

#draw list item background
img.blit(img_board, (0,0), (0,0))
img.blit(img_stone_w, target=(x_coor,y_coor), source=(0,0), mask=stoneMask)
img.blit(img_stone_b, target=(20, 40), source=(0,0), mask=stoneMask)
img.blit(img_stone_w, target=(20, 60), source=(0,0), mask=stoneMask)


img.blit(img_stone_b, target=(40, 20), source=(0,0), mask=stoneMask)
#img.blit(img_stone_w, target=(x_coor,y_coor), source=(0,0))
#draw list item text
#img.text((30,30),u'List Text',(0,0,0),"title")

# hide the virtual directional pad
appuifw.app.directional_pad=False;
canvas=appuifw.Canvas(event_callback=None, redraw_callback=handle_redraw)
appuifw.app.body=canvas

app_lock=e32.Ao_lock()
app_lock.wait()


