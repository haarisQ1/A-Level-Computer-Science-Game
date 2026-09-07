from ursina import *

app = Ursina()

#Creates an empty pivot as an entity
camera_pivot = Entity()
camera.parent = camera_pivot
camera.position = (0, 0, 0)
camera.rotation = (0, 0, 0)
camera.fov = 90

mouse.locked = True


ground = Entity(
    model='plane',
    color=color.rgb(139, 90, 60),
    scale=200,
    position=(0, -5, 0)
)

Sky()
DirectionalLight(y=10, z=10, rotation=(45, -45, 0), shadows=True)
AmbientLight(color=color.rgba(200, 200, 200, 255))
# Allows camera rotation using mouse inputs, and the clamp means you cannot look too far up or down
def update():
    camera_pivot.rotation_y += mouse.velocity[0] * 40
    camera_pivot.rotation_x -= mouse.velocity[1] * 40
    camera_pivot.rotation_x = clamp(camera_pivot.rotation_x, -80, 80)
# Quits application if escape key is hit
def input(key):
    if key == 'escape':
        mouse.locked = False
        application.quit()


app.run()