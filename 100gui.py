import appuifw, e32, graphics

#Define the exit function
def quit():app_lock.signal()
appuifw.app.exit_key_handler=quit
appuifw.app.screen='large'
selectedindex=0

def handle_redraw(rect):
     canvas.blit(img)

def handle_redraw(rect):
    global photo
    canvas.blit(photo)

def quit():
    app_lock.signal()


img=graphics.Image.new((360,640))

img2=graphics.Image.open("c:\\Data\\python\\board.jpg")
#img2=graphics.Image.open("e:\\Images\\area.png")

#draw list item background
img.blit(img2, (0,0), (0,0))
#draw list item text
img.text((30,30),u'List Text',(0,0,0),"title")

canvas=appuifw.Canvas(event_callback=None, redraw_callback=handle_redraw)
appuifw.app.body=canvas
canvas.bind(key_codes.EKeySelect, press_select)
canvas.bind(key_codes.EKeyDownArrow, press_down)
canvas.bind(key_codes.EKeyUpArrow, press_up)
canvas.bind(key_codes.EKeyRightArrow, press_right)
canvas.bind(key_codes.EKeyLeftArrow, press_left)

appuifw.app.exit_key_handler = quit
app_lock=e32.Ao_lock()
app_lock.wait()


