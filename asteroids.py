import pygame
import math
import time

VERSION = "0.0.1"
screen = None

CL_BLACK = (0, 0, 0)
CL_WHITE = (255, 255, 255)

    

class Screen():
    def __init__(self):
        self.width = 1000
        self.height = 800
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f"Asteroids - v{VERSION}")
        
    def update(self):
        self.screen.fill(CL_BLACK)
        pygame.display.update()
        
        
class Spaceship():
    def __init__(self):
        self.direction = 0
        self.position = (0, 0)
        self.bullets = []
        self.velocity = 0
        
        self.score = 0
        self.lives = 3
        
    def _draw(self):
        tip_length = 25
        wing_length = 40
        back_depth = 35
        
        tip_angle = math.radians(40) /2
        
        tip = (self.position[0] + tip_length*math.cos(self.direction), self.position[1] - tip_length*math.sin(self.direction))
        right_angle = self.direction + tip_angle
        left_angle = self.direction - tip_angle
        
        right_wing = (tip[0] - wing_length*math.cos(right_angle), tip[1] + wing_length*math.sin(right_angle))
        left_wing = (tip[0] - wing_length*math.cos(left_angle), tip[1] + wing_length*math.sin(left_angle))

        right_back = (tip[0] - back_depth*math.cos(right_angle), tip[1] + back_depth*math.sin(right_angle))
        left_back = (tip[0] - back_depth*math.cos(left_angle), tip[1] + back_depth*math.sin(left_angle))
        

        pygame.draw.line(screen.screen, CL_WHITE, self.position, tip, 2)
        pygame.draw.line(screen.screen, CL_WHITE, tip, right_wing, 2)
        pygame.draw.line(screen.screen, CL_WHITE, tip, left_wing, 2)
        pygame.draw.line(screen.screen, CL_WHITE, right_back, left_back, 2)
        
        pygame.display.update()
        
    def set_position(self, position):
        self.position = position
    
    def update(self):
        self._draw()
        
        
    def rotate(self, angle):
        rad = math.radians(angle)
        self.direction = rad
        self.update()
        
        
        
class Bullet():
    def __init__(self):
        self.direction = 0
        self.position = (0, 0)
        self.velocity = 0
        

            

def main():
    global screen 
    
    screen = Screen()
    player = Spaceship()
    
    player.set_position((screen.width / 2, screen.height / 2))
    player.update()
    
    for i in range(360):
        player.rotate(i)
        time.sleep(0.005)
        screen.update()
    pass


if __name__ == "__main__":
    main()