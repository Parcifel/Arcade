import pygame
import time
import sys
import math
import random

VERSION = "0.0.4"
DEBUG = False

CL_BLACK = (0, 0, 0)
CL_WHITE = (255, 255, 255)
CL_LIGHT_GRAY = (200, 200, 200)
CL_DARK_GRAY = (50, 50, 50)

DISPLAY = (1000, 800)
DEFAULT_FONT_SIZE = 20

pygame.font.init()
FONT_FAMILY = "Consolas"
SCORE_FONT = pygame.font.SysFont(FONT_FAMILY, 20)
SCORE_TOP_LEFT = (10, 10)
LIVES_TOP_LEFT = (10, 40)


TIP_LENGTH = 20
WING_LENGTH = 40
BACK_DEPTH = 30
TIP_ANGLE = math.radians(45) /2

LIFE_WIDTH = WING_LENGTH * math.sin(TIP_ANGLE) * 2
LIFE_HEIGHT = WING_LENGTH * math.cos(TIP_ANGLE)
LIFE_BACK_WIDTH = BACK_DEPTH * math.sin(TIP_ANGLE) * 2
LIFE_BACK_DEPTH = BACK_DEPTH * math.cos(TIP_ANGLE)

def draw_life(screen, top_left):
    tip = (top_left[0] + LIFE_WIDTH/2, top_left[1])
    right_wing = (top_left[0] + LIFE_WIDTH, top_left[1] + LIFE_HEIGHT)
    left_wing = (top_left[0], top_left[1] + LIFE_HEIGHT)
    right_back = (tip[0] + LIFE_BACK_WIDTH/2, tip[1] + LIFE_BACK_DEPTH)
    left_back = (tip[0] - LIFE_BACK_WIDTH/2, tip[1] + LIFE_BACK_DEPTH)
    
    life = [tip, right_wing, right_back, left_back, left_wing]
    pygame.draw.polygon(screen, CL_WHITE, life, 2)
    
    
class Screen:
    def __init__(self) -> None:
        self.width = DISPLAY[0]
        self.height = DISPLAY[1]
        
        self.screen = pygame.display.set_mode(DISPLAY)
        pygame.display.set_caption(f"Asteroids - v{VERSION}")
        
        self.player = Player(self.screen)
        self.player_bullets = []
        self.asteroids = []
        self.asteroids_wait = 1000
        self.saucers = []
        self.saucer_bullets = []
        
    def start(self):
        random_coordinates = [[random.randint(int(self.width*i/10), int(self.width*(i+1)/10)), random.randint(int(self.height*i/10), int(self.height*(i+1)/10))] for i in range(7)]
        for i, coordinate in enumerate(random_coordinates):
            while (coordinate[0] in range(int(self.width/2)-250, int(self.width/2)+250)) or (coordinate[1] in range(int(self.height/2)-100, int(self.height/2)+100)):
                coordinate[0] = random.randint(0, self.width)
                coordinate[1] = random.randint(0, self.height)
        
        for coordinate in range(len(random_coordinates)):
            direction = random.randint(0, 360)
            size = random.choice(["L", "M", "S"])
            self.asteroids.append(Asteroid(direction, random_coordinates[coordinate], self.screen, size))
            
        # text_height = 90
        # text_width = 30
        # inner_line_height = 10
            
        asteroids_text = [   
            [(257.5, 390), (257.5, 335), (280, 300), (302.5, 335), (302.5, 390), (302.5, 355), (257.5, 355)], #A
            [(312.5, 390), (357.5, 390), (357.5, 345), (312.5, 345), (312.5, 300), (357.5, 300)], #S
            [(367.5, 300), (412.5, 300), (390, 300), (390, 390)], #T
            [(467.5, 300), (422.5, 300), (422.5, 355), (467.5, 355), (422.5, 355), (422.5, 390), (467.5, 390)], #E 
            [(477.5, 390), (477.5, 300), (522.5, 300), (522.5, 355), (477.5, 355), (522.5, 390)], #R
            [(532.5, 390), (532.5, 300), (577.5, 300), (577.5, 390), (532.5, 390)], #O
            [(587.5, 300), (632.5, 300), (610, 300), (610, 390), (632.5, 390), (587.5, 390)], #I 
            [(642.5, 300), (665, 300), (687.5, 322.5), (687.5, 367.5), (665, 390), (642.5, 390), (642.5, 300)], #D
            [(697.5, 390), (742.5, 390), (742.5, 345), (697.5, 345), (697.5, 300), (742.5, 300)] #S
        ]
        
        press_to_play_text = [
            [(275, 460), (275, 410), (305, 410), (305, 440), (275, 440)], #P
            [(310, 460), (310, 410), (340, 410), (340, 440), (310, 440), (340, 460)], #R
            [(375, 410), (345, 410), (345, 440), (375, 440), (345, 440), (345, 460), (375, 460)], #E
            [(380, 460), (410, 460), (410, 435), (380, 435), (380, 410), (410, 410)], #S
            [(415, 460), (445, 460), (445, 435), (415, 435), (415, 410), (445, 410)], #S 
            [(485, 410), (515, 410), (500, 410), (500, 460)], #T
            [(520, 460), (520, 410), (550, 410), (550, 460), (520, 460)], #O
            [(590, 460), (590, 410), (620, 410), (620, 440), (590, 440)], #P
            [(625, 410), (625, 460), (655, 460)], #L
            [(660, 460), (660, 430), (675, 410), (690, 430), (690, 460), (690, 440), (660, 440)], #A
            [(695, 410), (710, 430), (725, 410), (710, 430), (710, 460)]  #Y
        ]
        
        for letter in asteroids_text:
            for point in range(len(letter)-1):
                pygame.draw.line(self.screen, CL_WHITE, letter[point], letter[point+1], 3)
                
        for letter in press_to_play_text:
            for point in range(len(letter)-1):
                pygame.draw.line(self.screen, CL_WHITE, letter[point], letter[point+1], 2)
        
        for asteroid in self.asteroids:
            asteroid._draw()
                
        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    waiting = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
                    break
                
        self.asteroids.clear()
        
    def run(self):
        self.start()
        
        while True:
            for event in pygame.event.get():
                #== QUIT ==#
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                #== MOVE ==# 
                elif event.type == pygame.MOUSEMOTION:
                    self.player.rotate(degrees=self.player.get_angle(event.pos))
                    
                #== KEY ==#
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player_bullets.append(Bullet(self.player.direction, self.player.tip, self.screen))
                    
                        
                    elif event.key == pygame.K_ESCAPE:
                        direction = random.randint(0, 360)
                        if direction in range(0, 90):
                            start = (0, random.randint(0, self.height))
                        elif direction in range(90, 180):
                            start = (random.randint(0, self.width), self.height)
                        elif direction in range(180, 270):
                            start = (self.width, random.randint(0, self.height))
                        else:
                            start = (random.randint(0, self.width), 0)
                            
                        direction -= 45
                        size = random.choice(["L", "M", "S"])
                        self.asteroids.append(Asteroid(direction, start, self.screen, size))
                    
                    else:
                        self.player.move(event_key=event.key)
                        
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        pass
                    else:
                        self.player.move(stop=event.key)
                    
            self.update()
            
            
    def update(self):
        self.screen.fill(CL_BLACK)
        
        self.player.update()
        
        if (len(self.asteroids) == 0) or (time.time() - self.asteroids[len(self.asteroids)-1].origin > self.asteroids_wait/1000):
            direction = random.randint(0, 360)
            
            if direction in range(0, 90):
                start = (0, random.randint(0, self.height))
            elif direction in range(90, 180):
                start = (random.randint(0, self.width), self.height)
            elif direction in range(180, 270):
                start = (self.width, random.randint(0, self.height))
            else:
                start = (random.randint(0, self.width), 0)
            
            direction -= 45
            size = random.choice(["L", "M", "S"])
            
            self.asteroids.append(Asteroid(direction, start, self.screen, size))
            
            if not( len(self.asteroids) > 10 ):
                self.asteroids_wait *= 0.99
            
            if self.asteroids_wait < 250:
                self.asteroids_wait = 250
            
        for bullet in self.player_bullets:
            position = bullet.get_position()
            
            if position[0] < 0 or position[0] > self.width:
                self.player_bullets.remove(bullet)
                del bullet
                continue
            elif position[1] < 0 or position[1] > self.height:
                self.player_bullets.remove(bullet)
                del bullet
                continue
            
            bullet.update()
        for asteroid in self.asteroids:
            radius = asteroid.get_radius()
            position = asteroid.get_position()
            
            if position[0] < -radius or position[0] > self.width+radius:
                self.asteroids.remove(asteroid)
                del asteroid
                continue
            elif position[1] < -radius or position[1] > self.height+radius:
                self.asteroids.remove(asteroid)
                del asteroid
                continue
            
            asteroid.update()
            
        
        for point in self.player.get_points():
            for asteroid in self.asteroids:
                if asteroid.collides_with(point):
                    self.asteroids.remove(asteroid)
                    del asteroid
                    self.player.die()
                    print(self.player.lives)
                    break
            
        for player_bullet in self.player_bullets:
            bullet_position = player_bullet.get_position()
            
            for asteroid in self.asteroids:
                if asteroid.collides_with(bullet_position) and player_bullet in self.player_bullets:
                    self.player_bullets.remove(player_bullet)
                    
                    astedoid_size = asteroid.get_size()
                    asteroid_position = asteroid.get_position()
                    asteroid_direction = asteroid.get_direction()
                    new_direction_1 = asteroid_direction + 45
                    new_direction_2 = asteroid_direction - 45
                    if astedoid_size == 10:
                        self.asteroids.append(Asteroid(new_direction_1, asteroid_position, self.screen, "M"))
                        self.asteroids.append(Asteroid(new_direction_2, asteroid_position, self.screen, "M"))    
                        self.player.score += 20                
                    elif astedoid_size == 8:
                        self.asteroids.append(Asteroid(new_direction_1, asteroid_position, self.screen, "S"))
                        self.asteroids.append(Asteroid(new_direction_2, asteroid_position, self.screen, "S"))
                        self.player.score += 10
                    else:
                        self.player.score += 5
                    
                    self.asteroids.remove(asteroid)
               
        text_surface = SCORE_FONT.render(f"Score: {self.player.score}", True, CL_WHITE)
        self.screen.blit(text_surface, SCORE_TOP_LEFT)
        
        current_life_top_left = LIVES_TOP_LEFT
        for life in range(self.player.lives):
            draw_life(self.screen, current_life_top_left)
            current_life_top_left = (current_life_top_left[0] + LIFE_WIDTH + 10, current_life_top_left[1])
        
        pygame.display.update()
        
        
class Player:
    def __init__(self, screen, lives=3, score=0) -> None:
        self.screen = screen
        
        self.direction = math.radians(0)
        self.position = (self.screen.get_width()/2, self.screen.get_height()/2)
        self.tip = 0
        self.points = []
        
        self.speed = 0.075
        self.velocity = [0, 0]
        self.last_key = [None, None]
        
        self.score = score
        self.lives = lives
        
        self.tip_length = TIP_LENGTH
        self.wing_length = WING_LENGTH
        self.back_depth = BACK_DEPTH
        
        self.tip_angle = TIP_ANGLE
        
        self.tip = (self.position[0] + self.tip_length, self.position[1])
        
        right_cos = math.cos( self.tip_angle )
        right_sin = math.sin( self.tip_angle )
        left_cos = math.cos( - self.tip_angle )
        left_sin = math.sin( - self.tip_angle )
        right_wing = (self.tip[0] - self.wing_length*right_cos, self.tip[1] + self.wing_length*right_sin)
        left_wing = (self.tip[0] - self.wing_length*left_cos, self.tip[1] + self.wing_length*left_sin)

        right_back = (self.tip[0] - self.back_depth*right_cos, self.tip[1] + self.back_depth*right_sin)
        left_back = (self.tip[0] - self.back_depth*left_cos, self.tip[1] + self.back_depth*left_sin)
        
        self.points.append(self.tip)
        self.points.append(right_wing)
        self.points.append(right_back)
        self.points.append(left_back)
        self.points.append(left_wing)
        
        
        
    def _draw(self):
        pygame.draw.polygon(self.screen, CL_WHITE, self.points, 2)
        
    def update(self):
        delta_x = self.velocity[0]
        delta_y = self.velocity[1]
        
        if self.position[0] < 0:
            delta_x += self.screen.get_width()
        elif self.position[0] > DISPLAY[0]:
            delta_x -= self.screen.get_width()
        if self.position[1] < 0:
            delta_y += self.screen.get_height()
        elif self.position[1] > DISPLAY[1]:
            delta_y -= self.screen.get_height()
            
        self.position = (self.position[0] + delta_x, self.position[1] + delta_y)
        for i, point in enumerate(self.points):
            self.points[i] = (point[0] + delta_x, point[1] + delta_y)
        self.tip = self.points[0]
        
        self._draw()
        
    def rotate(self, degrees=None, radians=None):
        if degrees is not None:
            self.direction = math.radians(degrees)
        else:
            self.direction = radians
        
        self.tip = (self.position[0] + self.tip_length*math.cos(self.direction), self.position[1] - self.tip_length*math.sin(self.direction))
        right_cos = math.cos( self.direction + self.tip_angle )
        right_sin = math.sin( self.direction + self.tip_angle )
        left_cos = math.cos( self.direction - self.tip_angle )
        left_sin = math.sin( self.direction - self.tip_angle )
        
        right_wing = (self.tip[0] - self.wing_length*right_cos, self.tip[1] + self.wing_length*right_sin)
        left_wing = (self.tip[0] - self.wing_length*left_cos, self.tip[1] + self.wing_length*left_sin)

        right_back = (self.tip[0] - self.back_depth*right_cos, self.tip[1] + self.back_depth*right_sin)
        left_back = (self.tip[0] - self.back_depth*left_cos, self.tip[1] + self.back_depth*left_sin)
        
        self.points = []
        self.points.append(self.tip)
        self.points.append(right_wing)
        self.points.append(right_back)
        self.points.append(left_back)
        self.points.append(left_wing)
        self.update()
    
    def get_angle(self, coordinate):
        delta_x = coordinate[0] - self.position[0]
        delta_y = -(coordinate[1] - self.position[1])
        
        if delta_x == 0 or delta_y == 0:
            if delta_x == 0:
                return 90 if delta_y > 0 else 270
            else:
                return 0 if delta_x > 0 else 180
        
        return math.degrees(math.atan2(delta_y, delta_x))
    
    def move(self, event_key=None, stop=None):
        # directions = ["U", "D", "L", "R"]
        
        if event_key is not None:
            if event_key == pygame.K_w:
                self.last_key[1] = pygame.K_w
            elif event_key == pygame.K_s:
                self.last_key[1] = pygame.K_s
            elif event_key == pygame.K_d:
                self.last_key[0] = pygame.K_d
            elif event_key == pygame.K_a:
                self.last_key[0] = pygame.K_a
        elif stop is not None:
            if stop == self.last_key[0]:
                self.last_key[0] = None
            elif stop == self.last_key[1]:
                self.last_key[1] = None
        else:
            return 
        
        for key in self.last_key:
            if event_key == pygame.K_w:
                self.velocity[1] -= self.speed
            elif event_key == pygame.K_s:
                self.velocity[1] += self.speed
            elif event_key == pygame.K_d:
                self.velocity[0] += self.speed
            elif event_key == pygame.K_a:
                self.velocity[0] -= self.speed
        
        if self.last_key[0] is None:
           self.velocity[0] = 0
        if self.last_key[1] is None:
            self.velocity[1] = 0 
        
        self.update()
        
    def get_points(self):
        return self.points
    
    def reset(self):
        self.position = (DISPLAY[0]/2, DISPLAY[1]/2)
        
        self.tip = (self.position[0] + self.tip_length, self.position[1])
        
        right_cos = math.cos( self.tip_angle )
        right_sin = math.sin( self.tip_angle )
        left_cos = math.cos( - self.tip_angle )
        left_sin = math.sin( - self.tip_angle )
        right_wing = (self.tip[0] - self.wing_length*right_cos, self.tip[1] + self.wing_length*right_sin)
        left_wing = (self.tip[0] - self.wing_length*left_cos, self.tip[1] + self.wing_length*left_sin)

        right_back = (self.tip[0] - self.back_depth*right_cos, self.tip[1] + self.back_depth*right_sin)
        left_back = (self.tip[0] - self.back_depth*left_cos, self.tip[1] + self.back_depth*left_sin)
        
        self.points.append(self.tip)
        self.points.append(right_wing)
        self.points.append(right_back)
        self.points.append(left_back)
        self.points.append(left_wing)
        pygame.draw.polygon(self.screen, CL_WHITE, self.points, 2)
        
    def die(self):
        self.lives -= 1
        
        if self.lives == -1:
            
            game_over_text = [
                [(402, 302), (402, 242), (327, 242), (327, 392), (402, 392), (402, 332), (372, 332)], #G
                [(417, 392), (417, 302), (454.5, 242), (492, 302), (492, 392), (492, 332), (417, 332)], #A 
                [(508, 392), (508, 242), (545.5, 302), (585, 242), (585, 392)], #M
                [(673, 242), (598, 242), (598, 332), (673, 332), (598, 332), (598, 392), (673, 392)], #E
                [(327, 558), (327, 408), (402, 408), (402, 558), (327, 558)], #O
                [(417, 408), (454.5, 558), (492, 408)], #V
                [(583, 408), (508, 408), (508, 498), (583, 498), (508, 498), (508, 558), (583, 558)], #E
                [(598, 558), (598, 408), (673, 408), (673, 498), (598, 498), (673, 558)]  #R
            ]
            
            
            for letter in game_over_text:
                for point in range(len(letter)-1):
                    pygame.draw.line(self.screen, CL_WHITE, letter[point], letter[point+1], 4)
            
            timer = 0
            stop = 3
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit() 
                        sys.exit()
                        
                pygame.display.update()
                time.sleep(0.1)
                timer += 0.1
                
                if timer >= stop:
                    break
            
            pygame.quit() 
            sys.exit()
            
        self.__init__(self.screen, self.lives, self.score)
        time.sleep(1)
        
        
        
        
class Bullet:
    def __init__(self, direction, start, screen):
        self.direction = direction
        self.position = start
        
        self.velocity = 0.2
        self.delta_x = self.velocity * math.cos(self.direction)
        self.delta_y = self.velocity * math.sin(self.direction)
        
        self.screen = screen
        self.radius = 4
        
        
    def update(self):
        self.position = (self.position[0] + self.delta_x, self.position[1] - self.delta_y)
        pygame.draw.circle(self.screen, CL_WHITE, self.position, self.radius)
        
    def get_position(self):
        return self.position
    
    def get_radius(self):
        return self.radius
    
class Asteroid():
    def __init__(self, direction, start, screen, size):
        self.screen = screen
        self.direction = math.radians(direction)
        self.position = start
        
        self.velocity = 0.1  
        self.delta_x = self.velocity * math.cos(self.direction)
        self.delta_y = self.velocity * math.sin(self.direction)
        self.corners = []
        
        self.origin = time.time()
        
        if size == "L":
            self.corner_count = 10
            self.radius = 40
                
        elif size == "M":
            self.corner_count = 8
            self.radius = 35
            
        elif size == "S":
            self.corner_count = 6
            self.radius = 25
        
        
        change = 360/(self.corner_count+1)
        for corner in range(self.corner_count):
            distance = random.randint(self.radius-5, self.radius+5)
            angle = corner*change + random.randint(0, int(change))
            
            d_x = distance * math.cos(math.radians(angle))
            d_y = distance * math.sin(math.radians(angle))
            
            self.corners.append((d_x, d_y))
            
    def update(self):
        self.position = (self.position[0] + self.delta_x, self.position[1] - self.delta_y)
        self._draw()
        
    def _draw(self):
        polygon = [(self.position[0]+corner[0], self.position[1]+corner[1]) for corner in self.corners]
        pygame.draw.polygon(self.screen, CL_WHITE, polygon, 2)
        
    def get_position(self):
        return self.position
    
    def get_radius(self):
        return self.radius
    
    def collides_with(self, coordinate):
        if (coordinate[0] > self.position[0]-self.radius) and (coordinate[0] < self.position[0]+self.radius):
            if (coordinate[1] > self.position[1]-self.radius) and (coordinate[1] < self.position[1]+self.radius):
                return True
        
        return False
    
    def get_size(self):
        return self.corner_count
    
    def get_direction(self):
        return math.degrees(self.direction)
    
    
        
if __name__ == "__main__":
    pygame.init()
    screen = Screen()
    screen.run()   