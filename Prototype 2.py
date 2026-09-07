from ursina import *

app = Ursina()

player = FirstPersonController()
player.gravity = 0
player.cursor.visible = False
# Creates ground
ground = Entity(
    model='plane',
    texture='grass',
    scale=100,
    collider='box'
)
# Creates sky
Sky()

def update():
    pass

def input(key):
    if key == 'escape':
        application.quit()


app.run()