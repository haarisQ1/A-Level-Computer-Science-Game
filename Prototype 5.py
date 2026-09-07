from ursina import *
import random

app = Ursina()

camera_pivot = Entity()
camera.parent = camera_pivot
camera.position = (0, 0, 0)
camera.fov = 90
mouse.locked = True

class TargetBall(Entity):
    def __init__(self, level):
        self.level = level
        self.size = max(0.5, 1.2 - (level * 0.05))
        
        super().__init__(
            model='sphere',
            color=color.red,
            scale=self.size,
            collider='sphere'
        )
        
        self.speed = 2.5 + (level * 0.5)
        self.direction = Vec3(random.choice([-1, 1]), 0, random.choice([-1, 1]))
        self.position = Vec3(random.uniform(-6, 6), 1, random.uniform(8, 14))
    
    def update(self):
        dt = time.dt
        
        self.x += self.direction.x * self.speed * dt
        self.z += self.direction.z * self.speed * dt
        
        if self.x > 10 or self.x < -10:
            self.direction.x *= -1
        
        if self.z > 16 or self.z < 6:
            self.direction.z *= -1

target = TargetBall(level=1)

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
