import pygame
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Player position and rotation
player_x, player_y = 5.0, 5.0
player_angle = 0.0
FOV = math.pi / 3  # 60 degrees

# Simple map (1 = wall, 0 = empty)
game_map = [
    [1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,0,0,1,0,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1]
]

def cast_ray(angle):
    # Cast a single ray and return distance to wall
    ray_x = player_x
    ray_y = player_y
    
    dx = math.cos(angle) * 0.1
    dy = math.sin(angle) * 0.1
    
    distance = 0
    while distance < 20:
        ray_x += dx
        ray_y += dy
        distance += 0.1
        
        map_x = int(ray_x)
        map_y = int(ray_y)
        
        if game_map[map_y][map_x] == 1:
            return distance
    
    return 20

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_angle -= 0.05
    if keys[pygame.K_RIGHT]:
        player_angle += 0.05
    
    screen.fill((0, 0, 0))
    
    # Render 3D view
    num_rays = 800
    for i in range(num_rays):
        ray_angle = player_angle - FOV/2 + (FOV * i / num_rays)
        distance = cast_ray(ray_angle)
        
        wall_height = min(600, int(21000 / (distance + 0.0001)))
        color_intensity = max(0, 255 - distance * 10)
        
        pygame.draw.line(screen, (color_intensity, color_intensity, color_intensity),
                        (i, 300 - wall_height//2), (i, 300 + wall_height//2))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()