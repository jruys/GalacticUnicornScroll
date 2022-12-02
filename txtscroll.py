import machine, time
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY

# Experimenting with scrolling text on Galactic Unicorn
# Jan-Willem Ruys, December 2022
#
# A/B - Change foreground color
# C/D - Change background color
# Vol - Change scroll speed
# Zzz - Pause scroll
# Lux - Change brightness

# overclock to 200Mhz
machine.freq(200000000)

# create galactic object and graphics surface for drawing
galactic = GalacticUnicorn()
graphics = PicoGraphics(DISPLAY)

# returns the id of the button that is currently pressed or
# None if none are
def pressed():
    if galactic.is_pressed(GalacticUnicorn.SWITCH_A):
        return GalacticUnicorn.SWITCH_A
    if galactic.is_pressed(GalacticUnicorn.SWITCH_B):
        return GalacticUnicorn.SWITCH_B
    if galactic.is_pressed(GalacticUnicorn.SWITCH_C):
        return GalacticUnicorn.SWITCH_C
    if galactic.is_pressed(GalacticUnicorn.SWITCH_D):
        return GalacticUnicorn.SWITCH_D
    if galactic.is_pressed(GalacticUnicorn.SWITCH_SLEEP):
        return GalacticUnicorn.SWITCH_SLEEP
    if galactic.is_pressed(GalacticUnicorn.SWITCH_VOLUME_UP):
        return GalacticUnicorn.SWITCH_VOLUME_UP
    if galactic.is_pressed(GalacticUnicorn.SWITCH_VOLUME_DOWN):
        return GalacticUnicorn.SWITCH_VOLUME_DOWN
    if galactic.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_UP):
        return GalacticUnicorn.SWITCH_BRIGHTNESS_UP
    if galactic.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_DOWN):
        return GalacticUnicorn.SWITCH_BRIGHTNESS_DOWN
    return None

graphics.set_font("bitmap8")

#Text='Het was in het allerholst van de nacht en twee grote volle manen stonden met verwijtende gezichten aan de hemel. Hoe hard rijden we nu? vroeg ik. Zesennegentig, zei Adriaan en draaide achteloos het stuur drie keer rond. Waar rijden we nu? vroeg ik. Om de markt in Rittenburg, zei Adriaan. Rittenburg is een prachtig oud stadje, zei ik. Het bezit een fraai middeleeuws stadhuis, met een monumentale trap. Nee, zei ik, toen het lawaai had opgehouden, het bezat een fraai middeleeuws stadhuis...'
Text='Far out in the uncharted backwaters of the unfashionable end of the western spiral arm of the Galaxy lies a small unregarded yellow sun. Orbiting this at a distance of roughly ninety-two million miles is an utterly insignificant little blue green planet whose ape-descended life forms are so amazingly primitive that they still think digital watches are a pretty neat idea...'
print("Text to render: "+Text)
Width=graphics.measure_text(Text,1,1)
print("Text width in pixels: "+str(Width))
Shadow=False # Set to True if you want a 1 pixel black border around the font, this slows down rendering
print("Shadow mode: "+str(Shadow))

pf=[[255,0,0],[0,255,0],[0,0,255],[255,255,0],[255,0,255],[0,255,255],[255,255,255]] # palette foreground
cf=0 # color index initial foreground
fr, fg, fb = pf[cf] # foreground r, g, b
print("Number of foreground colors: "+str(len(pf)))

pb=[[32,0,0],[0,32,0],[0,0,32],[32,32,0],[32,0,32],[0,32,32],[32,32,32],[0,0,0]] # palette background
cb=2 # color index initial background
br, bg, bb = pb[cb] # background r, g, b
print("Number of background colors: "+str(len(pb)))

ScrollSet=0.025
ScrollStep=0.005
ScrollMin=0
ScrollMax=0.25
print("Initial scroll speed: "+str(ScrollSet))

BrightSet=0.6
BrightStep=0.1
BrightMax=1.0
BrightMin=0.1
print("Initial brightness: "+str(BrightSet))
galactic.set_brightness(BrightSet)

# We use this flag to wait for key release when one has been pressed
KeyDown=False

while True:
  for Pos in range(53,-1*Width,-1):
    graphics.set_pen(graphics.create_pen(br, bg, bb))
    graphics.clear()
    if Shadow==True:
      graphics.set_pen(graphics.create_pen(0, 0, 0))
      graphics.text(Text, Pos-1, 2, -1, 1)
      graphics.text(Text, Pos+1, 2, -1, 1)
      graphics.text(Text, Pos, 1, -1, 1)
      graphics.text(Text, Pos, 3, -1, 1)
    graphics.set_pen(graphics.create_pen(fr, fg, fb))
    graphics.text(Text, Pos, 2, -1, 1)
    galactic.update(graphics)
    time.sleep(ScrollSet)
    
    if (KeyDown==False):
      if pressed()==GalacticUnicorn.SWITCH_A:
        print("A pressed - Next foreground color")
        KeyDown=True
        cf+=1
        if (cf>(len(pf)-1)):
          cf=0
        fr, fg, fb = pf[cf]
        print(pf[cf])

      if pressed()==GalacticUnicorn.SWITCH_B:
        print("B pressed - Previous foreground color")
        KeyDown=True
        cf-=1
        if (cf<0):
          cf=(len(pf)-1)
        fr, fg, fb = pf[cf]
        print(pf[cf])

      if pressed()==GalacticUnicorn.SWITCH_C:
        print("C pressed - Next background color")
        KeyDown=True
        cb+=1
        if (cb>(len(pb)-1)):
          cb=0
        br, bg, bb = pb[cb]
        print(pb[cb])

      if pressed()==GalacticUnicorn.SWITCH_D:
        print("D pressed - Previous background color")
        KeyDown=True
        cb-=1
        if (cb<0):
          cb=(len(pb)-1)
        br, bg, bb = pb[cb]
        print(pb[cb])

      if pressed()==GalacticUnicorn.SWITCH_VOLUME_UP:
        print("Vol+ pressed - Faster")
        KeyDown=True
        ScrollSet-=ScrollStep
        if (ScrollSet<ScrollMin):
          ScrollSet=ScrollMin
        print(ScrollSet)

      if pressed()==GalacticUnicorn.SWITCH_VOLUME_DOWN:
        print("Vol- pressed - Slower")
        KeyDown=True
        ScrollSet+=ScrollStep
        if (ScrollSet>ScrollMax):
          ScrollSet=ScrollMax
        print(ScrollSet)

      if pressed()==GalacticUnicorn.SWITCH_BRIGHTNESS_UP:
        print("Lux+ pressed - Brighter")
        KeyDown=True
        BrightSet+=BrightStep
        if (BrightSet>BrightMax):
          BrightSet=BrightMax
        galactic.set_brightness(BrightSet)
        print(BrightSet)

      if pressed()==GalacticUnicorn.SWITCH_BRIGHTNESS_DOWN:
        print("Lux- pressed - Dimmer")
        KeyDown=True
        BrightSet-=BrightStep
        if (BrightSet<BrightMin):
          BrightSet=BrightMin
        galactic.set_brightness(BrightSet)
        print(BrightSet)

    if (pressed()==GalacticUnicorn.SWITCH_SLEEP):
      print("ZZZ pressed - Pause scroll")
      while not (pressed()==None):
        time.sleep(0.01)

    if (KeyDown==True) and (pressed()==None):
      print("Key released")
      KeyDown=False

# the end
