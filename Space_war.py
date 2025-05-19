import pygame
import random


SCREEN_X, SCREEN_Y = 1000, 1000
COLOR_WHITE = (255, 255, 255)
COLOR_GRAY = (200, 200, 50)
COLOR_RED = (255, 0, 0)


def main():

    pygame.init()


    clock = pygame.time.Clock()
    contador = 0
    count = 200
    lives = 3
    laser_move = 1
    shot = False
    shieldc = 0
    shield = False
    game = True
    fase = 1
    vel = 0.5

    fuente = pygame.font.SysFont('Consolas', 30)

    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    pygame.display.set_caption('Space war')

    computer = pygame.image.load('Space_war\\assets\\Computer.png').convert_alpha()
    computer = pygame.transform.scale(computer,(SCREEN_X, SCREEN_Y))

    monitor_rect = pygame.Rect(177, 110, 650, 430)
    fondo = pygame.image.load('Space_war\\assets\\space.png').convert()    
    fondo_escalado = pygame.transform.scale(fondo, (monitor_rect.width, monitor_rect.height))
    monitor_surface = pygame.transform.scale(fondo, (monitor_rect.width, monitor_rect.height))

    class Nave:
        def __init__ (self, ruta, posicion):
            self.originalimg = pygame.image.load(ruta).convert_alpha()
            self.imagen = pygame.transform.scale(self.originalimg, (80, 60))
            self.rect = self.imagen.get_rect()
            self.rect.midbottom = posicion
            self.velocidady = 0
            self.velocidadx = 0
        def mover(self):
            self.rect.y += self.velocidady * delta_time
            self.rect.x += self.velocidadx * delta_time
        def draw(self, surface):
            surface.blit(self.imagen, self.rect)
        
    nave_normal = Nave('Space_war\\assets\\nave.png', (50, monitor_rect.height // 2))
    nave_normal.velocidad = 1
    nave_shot = Nave('Space_war\\assets\\nave2.png', nave_normal.rect.midbottom)
    nave_destroy = Nave('Space_war\\assets\\game_over.png', nave_normal.rect.midbottom)
    nave_shield = Nave('Space_war\\assets\\shield.png', nave_normal.rect.midbottom)
    
    class Pic:
        def __init__ (self, ruta, sice, pos):
            self.originalimg = pygame.image.load(ruta).convert_alpha()
            self.imagen = pygame.transform.scale(self.originalimg, sice)
            self.rect = self.imagen.get_rect()
            self.rect.midbottom = pos
            
        def draw(self, surface):
            surface.blit(self.imagen, self.rect)

    heart3 = Pic('Space_war\\assets\\corazon3.png', (80, 60), (50, 50))
    heart2 = Pic('Space_war\\assets\\corazon2.png', (80, 60), (50, 50))
    heart1 = Pic('Space_war\\assets\\corazon1.png', (80, 60), (50, 50))
    game_over = Pic('Space_war\\assets\\GAMEOVER.png', (400, 200), (monitor_rect.width // 2 + 20, monitor_rect.height // 2 + 100))
    youwin = Pic('Space_war\\assets\\youwin.png', (400, 200), (monitor_rect.width // 2 + 20, monitor_rect.height // 2 + 100))
    heart = Pic('Space_war\\assets\\heart.png', (80, 80), (0, 0))
    sild = Pic('Space_war\\assets\\sild.png', (80, 80),(0, 0))
    
    class Meteoritos:
        def __init__ (self, ruta, tamaño, posicion, velocidad):
            self.originalimg = pygame.image.load(ruta).convert_alpha()
            self.imagen = pygame.transform.scale(self.originalimg, (tamaño, tamaño))
            self.rect = self.imagen.get_rect()
            self.rect.midbottom = (posicion)
            self.velocidad = velocidad
            
        def mover(self):
            self.rect.x -= self.velocidad * delta_time

        def draw(self, surface):
            surface.blit(self.imagen, self.rect)

    boss = Meteoritos('Space_war\\assets\\boss.png', 300, (monitor_rect.width  + 100, monitor_rect.height // 2 + 100 ), 0)
    bosslive = 30

    class LaserBoss:
        #Copy Paste from tutorial
        def __init__ (self, origen, destino, velocidad):
            self.rect = pygame.Rect(origen[0], origen[1], 15, 5)
            self.velocidad = velocidad

            dx = destino[0] - origen[0] 
            dy = destino[1] - origen[1]
            distancia = (dx ** 2 + dy ** 2) ** 0.5
            self.vx = dx / distancia * velocidad
            self.vy = dy / distancia * velocidad

        def mover(self):
            self.rect.x += self.vx * delta_time
            self.rect.y += self.vy * delta_time
  
        def draw(self, surface):
            pygame.draw.rect(surface, COLOR_RED, laserboss)

    
    meteoritos = []
    power_ups = []
    power_uph = []
    lasers = []
    boss_att = []
    
#BUCLE

    while True:

        screen.fill(COLOR_WHITE)
        monitor_surface.fill(COLOR_WHITE)
        timer = pygame.time.get_ticks()
        game_time = int(20 - timer * 0.001)
        texto = fuente.render(str(game_time), True, COLOR_GRAY)

        delta_time = clock.tick(60)
        contador += delta_time

#CONTROLES Y MOVIMIENTO

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                
                if event.type == pygame.KEYDOWN and game == True:
                    if event.key == pygame.K_UP:
                        nave_normal.velocidady = -1
                    if event.key == pygame.K_DOWN:
                        nave_normal.velocidady = 1
                    if event.key == pygame.K_RIGHT:
                        nave_normal.velocidadx = 1
                    if event.key == pygame.K_LEFT:
                        nave_normal.velocidadx = -1
                    if event.key == pygame.K_SPACE:
                        laser = pygame.Rect(nave_normal.rect.centerx, nave_normal.rect.centery + 5, 10, 2)
                        lasers.append(laser)
                        shot = True

                        continue
                          
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        nave_normal.velocidady = 0
                    if event.key == pygame.K_DOWN:
                        nave_normal.velocidady = 0
                    if event.key == pygame.K_RIGHT:
                        nave_normal.velocidadx = 0
                    if event.key == pygame.K_LEFT:
                        nave_normal.velocidadx = 0
                    if event.key == pygame.K_SPACE:
                        shot = False
        
        nave_normal.mover()  

        if fase == 2 and bosslive > 0:
            boss.mover()  
            boss.rect.y += vel * delta_time             
                
        if nave_normal.rect.top < 0:
             nave_normal.rect.top = 0
        if nave_normal.rect.bottom > 430:
            nave_normal.rect.bottom = 430
        if nave_normal.rect.right > monitor_rect.width:
            nave_normal.rect.right = monitor_rect.width
        if nave_normal.rect.left < 0:
            nave_normal.rect.left = 0

        if boss.rect.left < (monitor_rect.width - 300):
            boss.rect.left = (monitor_rect.width - 300)
        if boss.rect.top < 0:
            vel *= -1
            boss.rect.top = 0
        if boss.rect.bottom > 430:
            vel *= -1
            boss.rect.bottom = 430
#GENERACION OBSTACULOS

        if fase == 1:
            if contador >1000 and game == True:
                danger = random.randint(1, 10)
                for i in range(danger):
                    tamaño = random.randint(40, 140)
                    if tamaño < 71:
                        meteor = Meteoritos ('Space_war\\assets\\meteor.png', tamaño, (monitor_rect.width + 10, random.randint(10, monitor_rect.height)), 1)
                    elif tamaño < 106:
                        meteor = Meteoritos ('Space_war\\assets\\meteor.png', tamaño, (monitor_rect.width + 10, random.randint(10, monitor_rect.height)), 0.7)
                    else:
                        meteor = Meteoritos ('Space_war\\assets\\meteor.png', tamaño, (  monitor_rect.width + 10, random.randint(10, monitor_rect.height)), 0.5)
                    meteoritos.append(meteor)

                if random.randint(0, 1) == 1:
                    contador = 0
                else:
                    contador = 500
            
        if fase == 2:
            boss.velocidad = 0.5
            count -= delta_time

            if boss.rect.left == (monitor_rect.width - 300) and count < 0 and bosslive > 0:
                origen = [boss.rect.centerx - 85, boss.rect.centery - 20]
                destino = nave_normal.rect.center
                laserboss = LaserBoss(origen, destino, 0.6)
                boss_att.append(laserboss)
                count = 150
                        
# MOVIMIENTO

        for meteor in meteoritos:
            meteor.mover()
        
        for laser in lasers:
            laser.x += laser_move * delta_time

        for laserboss in boss_att:
            laserboss.mover()
        for heart in power_uph:
            heart.mover()

        for sild in power_ups:
             sild.mover()

#COLISIONES

        for laser in lasers[:]:
            if laser.left > 660:
                lasers.remove(laser)
                continue
            if boss.rect.colliderect(laser):
                bosslive -=1
                lasers.remove(laser)
            for meteor in meteoritos[:]:
                if laser.colliderect(meteor.rect):
                    lasers.remove(laser)
                    luck = random.randint(1, 5)
                    if luck == 1:    
                        if random.randint(1, 2) == 1:
                            heart = Meteoritos('Space_war\\assets\\heart.png', 80, meteor.rect.midbottom, 0.5)
                            power_uph.append(heart)
                            meteoritos.remove(meteor)
                        elif random.randint(1, 2) == 2:     
                            sild = Meteoritos('Space_war\\assets\\sild.png', 80,meteor.rect.midbottom, 0.5)
                            power_ups.append(sild)
                            meteoritos.remove(meteor)
                    else:
                        meteoritos.remove(meteor)
                    break
        
        for laserboss in boss_att[:]:
            if nave_normal.rect.colliderect(laserboss):
                    if shield == False:
                        lives -= 1
                        shieldc = 2000
                        shield = True
                    boss_att.remove(laserboss)
            if laserboss.rect.right < 0:
                boss_att.remove(laserboss)
        
        if boss.rect.colliderect(nave_normal.rect):
            if shield == False:
                        lives -= 1
                        shieldc = 2000
                        shield = True

        for meteor in meteoritos[:]:
            if nave_normal.rect.colliderect(meteor.rect):
                    if shield == False:
                        lives -= 1
                        shieldc = 2000
                        shield = True
                    meteoritos.remove(meteor)
            if meteor.rect.x < 0:
                meteoritos.remove(meteor)
            
        for heart in power_uph[:]:
            if nave_normal.rect.colliderect(heart.rect):
                    if lives < 3:
                        lives += 1
                        power_uph.remove(heart)
                    else:
                        power_uph.remove(heart)
            if heart.rect.x < 0:
                power_uph.remove(heart)

        for sild in power_ups[:]:
            if nave_normal.rect.colliderect(sild.rect):
                    shieldc = 2000
                    shield = True
                    power_ups.remove(sild)
            if sild.rect.x < 0:
                power_ups.remove(sild)

#EVENTOS
              
        if shield == True:
            shieldc -= delta_time
            if shieldc < 0:
                shield = False

        if game_time < 0:
            fase = 2
#PANTALLA
 
        clock.tick(60)

        screen.blit(computer, (0, 0))
        monitor_surface.blit(fondo_escalado, (0, 0))
        if fase == 1:
            monitor_surface.blit(texto, (monitor_rect.width // 2, 10))
        elif fase == 2 and bosslive > 0:
            texto = fuente.render('DANGER', True, COLOR_RED)
            monitor_surface.blit(texto, (monitor_rect.width // 2, 10))

        if lives == 3:
            heart3.draw(monitor_surface)
        elif lives == 2:
            heart2.draw(monitor_surface)
        elif lives == 1:
            heart1.draw(monitor_surface)
        elif lives == 0:
            game = False

        nave_normal.draw(monitor_surface)

        if shot == True:
            nave_shot.rect.midbottom = nave_normal.rect.midbottom
            nave_shot.draw(monitor_surface)
        if shield == True and lives > 0:
            nave_shield.rect.midbottom = nave_normal.rect.midbottom
            nave_shield.draw(monitor_surface)

        for laser in lasers: 
            pygame.draw.rect(monitor_surface, COLOR_RED, laser)
        for meteor in meteoritos :
            meteor.draw(monitor_surface)
        for heart in power_uph[:]:
            heart.draw(monitor_surface)     
        for sild in power_ups[:]:
            
            sild.draw(monitor_surface)
        if fase == 2 and bosslive > 0:
            boss.draw(monitor_surface)  
            for laserboss in boss_att:
                laserboss.draw(monitor_surface)

        
        if game == False and bosslive > 0:
            nave_destroy.rect.midbottom = nave_normal.rect.midbottom
            nave_destroy.draw(monitor_surface)
            game_over.draw(monitor_surface) 
        
        if bosslive < 1:
            game = False
            youwin.draw(monitor_surface)

        screen.blit(monitor_surface, (monitor_rect.x, monitor_rect.y))
          
        pygame.display.flip()

        

if __name__ == '__main__':
    main()

