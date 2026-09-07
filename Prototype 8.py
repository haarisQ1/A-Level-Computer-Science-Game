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
        
        self.vertical_speed = 0.2 + (level * 0.15)
        self.vertical_direction = random.choice([-1, 1])
        self.base_height = 1
        self.vertical_range = 0.5 + (level * 0.2)
    
    def update(self):
        dt = time.dt
        
        self.x += self.direction.x * self.speed * dt
        self.z += self.direction.z * self.speed * dt
        self.y += self.vertical_direction * self.vertical_speed * dt
        
        if abs(self.x) > 10:
            self.x = 10 if self.x > 0 else -10
            self.direction.x *= -1
        
        if self.z > 16 or self.z < 6:
            self.z = clamp(self.z, 6, 16)
            self.direction.z *= -1
        
        if self.y > self.base_height + self.vertical_range:
            self.y = self.base_height + self.vertical_range
            self.vertical_direction = -1
        elif self.y < self.base_height - self.vertical_range:
            self.y = self.base_height - self.vertical_range
            self.vertical_direction = 1

target = TargetBall(level=1)
score = 0
tracking = False

# Laser beam entity
laser = Entity(
    model='cube',
    color=color.rgba(255, 255, 0, 200),
    scale=(0.02, 0.02, 200),
    visible=False,
    unlit=True
)

# Laser dot to show hit point
laser_dot = Entity(
    model='sphere',
    color=color.yellow,
    scale=0.2,
    visible=False,
    unlit=True
)

Sky()
ground = Entity(model='plane', color=color.rgb(139, 90, 60), scale=200, position=(0, -5, 0))
DirectionalLight(y=10, z=10, rotation=(45, -45, 0))

score_text = Text(text=f'Score: {score}', position=(-0.85, 0.45), scale=2)

def update():
    global score, tracking
    
    camera_pivot.rotation_y += mouse.velocity[0] * 40
    camera_pivot.rotation_x -= mouse.velocity[1] * 40
    camera_pivot.rotation_x = clamp(camera_pivot.rotation_x, -80, 80)
    
    # Continuous laser while holding mouse
    if held_keys['left mouse']:
        ray = raycast(camera.world_position, camera.forward, distance=200)
        
        if ray.hit:
            laser_origin = camera.world_position
            hit_point = ray.world_point
            beam_vec = hit_point - laser_origin
            beam_len = beam_vec.length()
            
            # Make laser VISIBLE
            laser.visible = True
            laser.position = laser_origin + beam_vec * 0.5
            laser.look_at(hit_point)
            laser.scale = (0.02, 0.02, beam_len)
            
            # Show dot at hit point
            laser_dot.visible = True
            laser_dot.position = hit_point
            
            # Score tracking
            if ray.entity == target:
                score += 3
                score_text.text = f'Score: {score}'
                laser.color = color.rgba(0, 255, 0, 200)  # Green
                tracking = True
            else:
                laser.color = color.rgba(255, 255, 0, 200)  # Yellow
                tracking = False
        else:
            laser_origin = camera.world_position
            far_point = camera.world_position + camera.forward * 200
            beam_vec = far_point - laser_origin
            
            laser.visible = True
            laser.position = laser_origin + beam_vec * 0.5
            laser.look_at(far_point)
            laser.scale = (0.02, 0.02, 200)
            laser.color = color.rgba(255, 255, 0, 200)
            laser_dot.visible = False
            tracking = False
    else:
        laser.visible = False
        laser_dot.visible = False
        tracking = False

def input(key):
    if key == 'escape':
        mouse.locked = False
        application.quit()

app.run()
