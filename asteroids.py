import sys
import pygame
import math
import time

VERSION = "0.0.1"
screen = None

CL_BLACK = (0, 0, 0)
CL_WHITE = (255, 255, 255)


        
        
class Spaceship():
    def __init__(self, display):
        self.direction = 0
        self.position = (0, 0)
        self.bullets = []
        self.velocity = 0
        
        self.score = 0
        self.lives = 3
        self.screen = display
        
    def _draw(self):
        global screen
        
        tip_length = 20
        wing_length = 40
        back_depth = 30
        
        tip_angle = math.radians(45) /2
        
        tip = (self.position[0] + tip_length*math.cos(self.direction), self.position[1] - tip_length*math.sin(self.direction))
        right_angle = self.direction + tip_angle
        left_angle = self.direction - tip_angle
        
        right_wing = (tip[0] - wing_length*math.cos(right_angle), tip[1] + wing_length*math.sin(right_angle))
        left_wing = (tip[0] - wing_length*math.cos(left_angle), tip[1] + wing_length*math.sin(left_angle))

        right_back = (tip[0] - back_depth*math.cos(right_angle), tip[1] + back_depth*math.sin(right_angle))
        left_back = (tip[0] - back_depth*math.cos(left_angle), tip[1] + back_depth*math.sin(left_angle))
        

        pygame.draw.line(self.screen, CL_WHITE, self.position, tip, 2)
        pygame.draw.line(self.screen, CL_WHITE, tip, right_wing, 2)
        pygame.draw.line(self.screen, CL_WHITE, tip, left_wing, 2)
        pygame.draw.line(self.screen, CL_WHITE, right_back, left_back, 2)
        
        pygame.display.update()
        
    def set_position(self, position):
        self.position = position
        self.update()
    
    def update(self):
        self._draw()
        
    def get_angle(self, coordinate):
        delta_x = coordinate[0] - self.position[0]
        delta_y = -(coordinate[1] - self.position[1])
        
        print(f'\ncx: {self.position[0]}, cy: {self.position[1]}\ndx: {delta_x}, dy: {delta_y}\n')
        
        if delta_x == 0 or delta_y == 0:
            distance = math.sqrt(delta_x**2 + delta_y**2)
            if delta_x == 0:
                return 90 if delta_y > 0 else 270
            else:
                return 0 if delta_x > 0 else 180
        
        return math.degrees(math.atan2(delta_y, delta_x))
        
    def rotate(self, angle):
        rad = math.radians(angle)
        self.direction = rad
        self.update()
        
        
        
class Bullet():
    def __init__(self):
        self.direction = 0
        self.position = (0, 0)
        self.velocity = 0
        
        
class Screen():
    def __init__(self):
        self.width = 1000
        self.height = 800
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f"Asteroids - v{VERSION}")

        self.player = Spaceship(self.screen)
        self.player.set_position((self.width/2, self.height/2))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEMOTION:
                    self.player.rotate(self.player.get_angle(event.pos))
                    
            self.screen.fill(CL_BLACK)
            self.player.update()
        


def main():
    display = Screen()
    display.run()
    
    # pygame_init()
    # player = Spaceship()
    
    # player.set_position((DISPLAY_DIM[0]/2, DISPLAY_DIM[1]/2))
    # player.update()
    
    # for i in range(360):
    #     player.rotate(i)
    #     time.sleep(0.005)
    #     screen.fill(CL_BLACK)
    #     pygame.display.update()
    # pass

    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()
                
    #         if event.type == pygame.MOUSEMOTION:
    #             player.rotate(player.get_angle(event.pos))
            
    #     screen.fill(CL_BLACK)
    #     pygame.display.update()


if __name__ == "__main__":
    main()