from ursina import *
import random

app = Ursina()

camera_pivot = Entity()
camera.parent = camera_pivot
camera.position = (0, 0, 0)
camera.fov = 90
mouse.locked = True

class TargetBall(Entity):
    def __init__(self):
        super().__init__(
            model='sphere',
            color=color.red,
            scale=1.0,
            collider='sphere'
        )
        self.position = Vec3(
            random.uniform(-8, 8),
            random.uniform(0, 3),
            random.uniform(8, 16)
        )

target = TargetBall()

Sky()
ground = Entity(model='plane', color=color.rgb(139, 90, 60), scale=200, position=(0, -5, 0))
DirectionalLight(y=10, z=10, rotation=(45, -45, 0), shadows=True)

def update():
    camera_pivot.rotation_y += mouse.velocity[0] * 40
    camera_pivot.rotation_x -= mouse.velocity[1] * 40
    camera_pivot.rotation_x = clamp(camera_pivot.rotation_x, -80, 80)

def input(key):
    if key == 'escape':
        mouse.locked = False
        application.quit()

app.run()