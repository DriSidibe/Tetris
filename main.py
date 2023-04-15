"""
AUTHOR : SIDIBE drissa
"""

import random
from copy import deepcopy
from time import time
import pygame

pygame.init()


class Tetris:
    def __init__(self, resolution, isWindowOpen=True):
        self.nextColor = 0
        self.isHelpButtonPressed = False
        self.gameOver = False
        self.isGameMuted = False
        self.score = 0
        self.hightScore = 0
        self.fallingSpeed = 1
        self.collideLeft = False
        self.vitesse = 1
        self.resolution2 = resolution
        self.resolution = (300, 600)
        self.window = pygame.display.set_mode(resolution)
        self.isWindowOpen = isWindowOpen
        self.gridColor = (50, 50, 50)
        self.gridMatrix = list()
        self.gridMatrixCopy = list()
        self.buttonLeftRelease = True
        self.buttonRightRelease = True
        self.rapidFalling = False
        self.startTime = time()
        self.startTime2 = time()
        self.entranceStartTime = time()
        self.currentShape = 0
        self.nextCurrentShape = 0
        self.currentShapeX = 0
        self.nextCurrentShapeX = 0
        self.currentShapeY = 0
        self.nextCurrentShapeY = 0
        self.currentNumber = 0
        self.nextCurrentNumber = 0
        self.isSceneAnimationFinish = False
        self.startPlaying = False
        self.fps = pygame.time.Clock()
        self.collide = False
        self.color = random.randint(1, 8)
        self.numberOfLineCompleted = 0
        self.lines = list()
        self.logo = pygame.image.load('assets/images/logo.png').convert()
        self.pause_image = pygame.image.load('assets/images/pause.png').convert()
        self.home_image = pygame.image.load('assets/images/home.png').convert()
        self.volume_image = pygame.image.load('assets/images/volume.png').convert()
        self.help_image = pygame.image.load('assets/images/help.png').convert()
        self.isGamePaused = False
        self.helpMessage = []

        self.message = "COMMENT JOUER ?/-utilisez les touches directionnelles gauche et droite /pour vous " \
                       "deplacer./-utilisez la touche directionnelle bas pour faire /deplacer la brique de manière " \
                       "rapide./-utilisez la touche r pour faire tourner la brique./-maintener les touches " \
                       "directionnelles gauche et /droite pour vous deplacer rapidement vers la gauche /ou vers la " \
                       "droite./-en cas de perte, appuyer dur la touche espace pour/rejouer. "
        self.helpMessage = self.message.split("/")

        pygame.display.set_caption("teris")
        pygame.display.set_icon(pygame.image.load('assets/images/icon_litle.png'))

        self.barre = [
            [
                [1],
                [1],
                [1],
                [1],
                (1, 4)
            ],
            [
                [1, 1, 1, 1],
                (4, 1)
            ]
        ]
        self.carre = [
            [
                [1, 1],
                [1, 1],
                (2, 2)
            ]
        ]
        self.point = [
            [
                [1],
                (1, 1)
            ]
        ]
        self.T = [
            [
                [1, 0],
                [1, 1],
                [1, 0],
                (2, 3)
            ],
            [
                [1, 1, 1],
                [0, 1, 0],
                (3, 2)
            ],
            [
                [0, 1],
                [1, 1],
                [0, 1],
                (2, 3)
            ],
            [
                [0, 1, 0],
                [1, 1, 1],
                (3, 2)
            ]
        ]
        self.L = [
            [
                [1, 0],
                [1, 0],
                [1, 1],
                (2, 3)
            ],
            [
                [1, 1, 1],
                [1, 0, 0],
                (3, 2)
            ],
            [
                [1, 1],
                [0, 1],
                [0, 1],
                (2, 3)
            ],
            [
                [0, 0, 1],
                [1, 1, 1],
                (3, 2)
            ],
            [
                [0, 1],
                [0, 1],
                [1, 1],
                (2, 3)
            ],
            [
                [1, 0, 0],
                [1, 1, 1],
                (3, 2)
            ],
            [
                [1, 1],
                [1, 0],
                [1, 0],
                (2, 3)
            ],
            [
                [1, 1, 1],
                [0, 0, 1],
                (3, 2)
            ]
        ]
        self.Z = [
            [
                [0, 1],
                [1, 1],
                [1, 0],
                (2, 3)
            ],
            [
                [1, 1, 0],
                [0, 1, 1],
                (3, 2)
            ],
            [
                [1, 0],
                [1, 1],
                [0, 1],
                (2, 3)
            ],
            [
                [0, 1, 1],
                [1, 1, 0],
                (3, 2)
            ],
        ]
        self.dico = {1: self.barre, 2: self.carre, 3: self.T, 4: self.L, 5: self.Z, 6: self.point}
        self.dicoColor = {1: 'red', 2: 'blue', 3: 'green', 4: 'yellow', 5: 'white', 6: 'pink', 7: 'brown', 8: 'purple'}

        # fonts
        self.easyFont = pygame.font.SysFont('Verdana', 15)
        self.mediumFont = pygame.font.SysFont('Verdana', 15)
        self.hardFont = pygame.font.SysFont('Verdana', 15)
        self.pauseFont = pygame.font.SysFont('Verdana', 15)
        self.scoreFont = pygame.font.SysFont('Verdana', 15)
        self.hightScoreFont = pygame.font.SysFont('Verdana', 15)
        self.ScoreFont = pygame.font.SysFont('Verdana', 15)
        self.HightScoreFont = pygame.font.SysFont('Verdana', 15)
        self.gameOverFont = pygame.font.SysFont('Verdana', 30)
        self.helpMessageFont = pygame.font.SysFont('Verdana', 15)

        self.read_best_score()

        # fonts reders
        self.easyFontRender = self.easyFont.render("Facile", True, 'blue')
        self.mediumFontRender = self.mediumFont.render("Moyen", True, 'blue')
        self.hardFontRender = self.hardFont.render("Difficile", True, 'blue')
        self.pauseFontRender = self.hardFont.render("PAUSE", True, 'white')
        self.scoreFontRender = self.hardFont.render(str(self.score), True, 'white')
        self.hightScoreFontRender = self.hardFont.render(str(self.hightScore), True, 'white')
        self.ScoreFontRender = self.hardFont.render('SCORE :', True, 'yellow')
        self.HightScoreFontRender = self.hardFont.render('HIGHT SCORE :', True, 'yellow')
        self.gameOverFontRender = self.hardFont.render('GAME OVER !', True, 'yellow')
        self.helpMessageFontRenderList = []

        for message in self.helpMessage:
            self.helpMessageFontRenderList.append(self.helpMessageFont.render(message, True, 'white'))

    def main(self):
        pygame.mixer.init()
        pygame.mixer.music.load("assets/musiques/musique.ogg")
        pygame.mixer.music.play(100000000, 0.0)
        self.init_game()
        while self.isWindowOpen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isWindowOpen = False
                    pygame.quit()
                if not self.isGamePaused:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.buttonLeftRelease = False
                            self.startTime2 = time()
                            self.rapid_move_left()
                        if event.key == pygame.K_RIGHT:
                            self.buttonRightRelease = False
                            self.startTime2 = time()
                            self.rapid_move_right()
                        if event.key == pygame.K_DOWN:
                            self.rapidFalling = True
                        if event.key == pygame.K_r:
                            self.rotate()
                        if event.key == pygame.K_SPACE:
                            if self.gameOver:
                                self.replay()
                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            self.buttonLeftRelease = True
                            self.startTime2 = time()
                        if event.key == pygame.K_RIGHT:
                            self.buttonRightRelease = True
                            self.startTime2 = time()
                        if event.key == pygame.K_DOWN:
                            self.rapidFalling = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 200 <= pygame.mouse.get_pos()[0] <= 300:
                        if 150 <= pygame.mouse.get_pos()[1] <= 200:
                            self.button_easy_pressed()
                        elif 250 <= pygame.mouse.get_pos()[1] <= 300:
                            self.button_medium_pressed()
                        elif 350 <= pygame.mouse.get_pos()[1] <= 400:
                            self.button_hard_pressed()
                    elif 20 <= pygame.mouse.get_pos()[1] <= 40:
                        if self.resolution2[0] - 40 <= pygame.mouse.get_pos()[0] <= self.resolution2[0] - 20:
                            self.pause()
                        elif self.resolution2[0] - 80 <= pygame.mouse.get_pos()[0] <= self.resolution2[0] - 60:
                            self.mute()
                        elif self.resolution[0] + 20 <= pygame.mouse.get_pos()[0] <= self.resolution[0] + 40:
                            self.home()
                        elif self.resolution[0] + 60 <= pygame.mouse.get_pos()[0] <= self.resolution[0] + 80:
                            self.help()

            if self.isWindowOpen:
                self.window.fill('black')

                if self.startPlaying:
                    self.draw_grid()
                    self.draw_side_elements()
                    self.draw_bricks()
                    if self.isHelpButtonPressed:
                        self.draw_help()

                    if not self.gameOver:
                        if not self.isGamePaused:
                            self.bottom_side_gate()
                            self.rapid_move()
                            self.collision(self.currentShapeX, self.currentShapeY, self.currentNumber,
                                           self.currentShape)
                            self.collide = False

                            if not self.rapidFalling:
                                if time() - self.startTime >= self.fallingSpeed:
                                    self.auto_fall()
                                    self.startTime = time()
                            else:
                                self.auto_fall()

                if not self.startPlaying:
                    if not self.isSceneAnimationFinish:
                        if time() - self.entranceStartTime > 3:
                            self.isSceneAnimationFinish = True
                        else:
                            self.entrance_scene()
                    else:
                        self.menu()

                self.fps.tick(60)

                pygame.display.flip()

    def read_best_score(self):
        self.hightScore = open('bestScore.txt', 'r').readline()
        self.hightScoreFontRender = self.hardFont.render(str(self.hightScore), True, 'white')

    def update_best_score(self):
        if self.score > int(open('bestScore.txt', 'r').readline()):
            open('bestScore.txt', 'w').write(str(self.score))

    def draw_side_elements(self):
        if self.isGamePaused:
            self.window.blit(self.pauseFontRender, (
                (self.resolution[0] + (160 - self.pauseFontRender.get_width()) / 2, 150)))
        if self.gameOver:
            self.window.blit(self.gameOverFontRender, (
                (self.resolution[0] + (
                        self.resolution2[0] - self.resolution[0] - self.gameOverFontRender.get_width()) / 2, 200)))
        self.window.blit(self.volume_image, (
            (self.resolution2[0] - 80, 20)))
        self.window.blit(self.pause_image, (
            (self.resolution2[0] - 40, 20)))
        self.window.blit(self.home_image, (
            (self.resolution[0] + 20, 20)))
        self.window.blit(self.help_image, (
            (self.resolution[0] + 60, 20)))
        pygame.draw.line(self.window, 'white', (self.resolution[0] + 10, 50), (self.resolution2[0] - 10, 50), 2)
        self.window.blit(self.ScoreFontRender, (
            (self.resolution[0] + 40, 80)))
        self.window.blit(self.HightScoreFontRender, (
            (self.resolution[0] + 20, 100)))
        self.window.blit(self.scoreFontRender, (
            (self.resolution[0] + self.ScoreFontRender.get_width() + 60, 80)))
        self.window.blit(self.hightScoreFontRender, (
            (self.HightScoreFontRender.get_width() + self.resolution[0] + 30, 100)))
        self.draw_current_element()

    def draw_current_element(self):
        origin = self.resolution[0] + (
                (self.resolution2[0] - self.resolution[0]) - self.dico[self.nextCurrentNumber][self.nextCurrentShape][-1][
            0] * 20) / 2
        for i in range(len(self.dico[self.nextCurrentNumber][self.nextCurrentShape]) - 1):
            for j in range(len(self.dico[self.nextCurrentNumber][self.nextCurrentShape][i])):
                if self.dico[self.nextCurrentNumber][self.nextCurrentShape][i][j] != 0:
                    pygame.draw.rect(self.window,
                                     self.dicoColor[self.nextColor],
                                     (origin + j * 20, origin + i * 20, 20, 20))

    def pause(self):
        if not self.gameOver:
            if not self.isHelpButtonPressed:
                self.isGamePaused = not self.isGamePaused
                if self.isGamePaused:
                    self.pause_image = pygame.image.load('assets/images/play.png').convert()
                else:
                    self.pause_image = pygame.image.load('assets/images/pause.png').convert()

    def help(self):
        if not self.gameOver:
            if not self.isGamePaused:
                self.pause()
            self.isHelpButtonPressed = not self.isHelpButtonPressed

    def mute(self):
        self.isGameMuted = not self.isGameMuted
        if self.isGameMuted:
            pygame.mixer.music.pause()
            self.volume_image = pygame.image.load('assets/images/mute.png').convert()
        else:
            pygame.mixer.music.unpause()
            self.volume_image = pygame.image.load('assets/images/volume.png').convert()

    def home(self):
        self.isGamePaused = False
        self.startPlaying = False
        self.gridMatrix.clear()
        self.gridMatrixCopy.clear()
        self.grid_matrix_filler()
        self.choose_shape()
        self.pause_image = pygame.image.load('assets/images/pause.png').convert()
        self.update_best_score()
        self.score = 0
        self.scoreFontRender = self.hardFont.render(str(self.score), True, 'white')
        self.read_best_score()
        self.gameOver = False
        self.isHelpButtonPressed = False

    def button_easy_pressed(self):
        self.fallingSpeed = 0.8
        self.startPlaying = True

    def button_medium_pressed(self):
        self.fallingSpeed = 0.5
        self.startPlaying = True

    def button_hard_pressed(self):
        self.fallingSpeed = 0.15
        self.startPlaying = True

    def entrance_scene(self):
        self.window.blit(self.logo, (
            (self.resolution2[0] - self.logo.get_width()) / 2, (self.resolution2[1] - self.logo.get_height()) / 2))

    def menu(self):
        pygame.draw.rect(self.window, 'blue',
                         (((self.resolution2[0] - 300) / 2), ((self.resolution2[1] - 400) / 2), 300, 400), 2)
        pygame.draw.rect(self.window, 'white',
                         (((self.resolution2[0] - 100) / 2), ((self.resolution2[1] - 400) / 2 + 50), 100, 50))
        pygame.draw.rect(self.window, 'white',
                         (((self.resolution2[0] - 100) / 2), ((self.resolution2[1] - 400) / 2 + 150), 100, 50))
        pygame.draw.rect(self.window, 'white',
                         (((self.resolution2[0] - 100) / 2), ((self.resolution2[1] - 400) / 2 + 250), 100, 50))
        self.window.blit(self.easyFontRender, [(self.resolution2[0] - self.easyFontRender.get_width()) / 2, (
                (self.resolution2[1] - 400) / 2 + (50 - self.easyFontRender.get_height()) / 2) + 50])
        self.window.blit(self.mediumFontRender, [(self.resolution2[0] - self.mediumFontRender.get_width()) / 2, (
                (self.resolution2[1] - 400) / 2 + (50 - self.mediumFontRender.get_height()) / 2) + 150])
        self.window.blit(self.hardFontRender, [(self.resolution2[0] - self.hardFontRender.get_width()) / 2, (
                (self.resolution2[1] - 400) / 2 + (50 - self.hardFontRender.get_height()) / 2) + 250])

    def bricks_color(self, number):
        for i in self.dico[number]:
            for j in range(len(i)):
                if j != len(i) - 1:
                    for k in range(len(i[j])):
                        if i[j][k] != 0:
                            i[j][k] = self.color

    def draw_grid(self):
        for i in range(1, int(self.resolution[0] / 20) + 1):
            pygame.draw.line(self.window, self.gridColor, (i * 20, 0), (i * 20, self.resolution[1]))
        for i in range(1, int(self.resolution[1] / 20)):
            pygame.draw.line(self.window, self.gridColor, (0, i * 20), (self.resolution[0], i * 20))

    def draw_bricks(self):
        for i in range(int(len(self.gridMatrix))):
            for j in range(int(len(self.gridMatrix[i]))):
                if self.gridMatrix[i][j] != 0:
                    pygame.draw.rect(self.window, self.dicoColor[self.gridMatrix[i][j]], (j * 20, i * 20, 20, 20))

    def grid_matrix_filler(self):
        liste = list()
        for i in range(int(self.resolution[1] / 20)):
            for j in range(int(self.resolution[0] / 20)):
                liste.append(0)
            self.gridMatrix.append(liste.copy())
            liste.clear()
        self.gridMatrixCopy = deepcopy(self.gridMatrix)

    def next_shape(self):
        self.currentNumber = self.nextCurrentNumber
        self.currentShape = self.nextCurrentShape
        self.currentShapeX = self.nextCurrentShapeX
        self.currentShapeY = self.nextCurrentShapeY
        self.color = self.nextColor
        self.bricks_color(self.currentNumber)
        self.redraw(self.nextCurrentShapeX, self.nextCurrentShapeY, self.nextCurrentNumber, self.nextCurrentShape)

    def choose_shape(self):
        self.next_shape()
        self.nextCurrentNumber = random.randint(1, 5)
        self.nextColor = random.randint(1, 8)
        self.nextCurrentShape = 0
        self.nextCurrentShapeX = random.randint(0, int(self.resolution[0] / 20) - 2)
        self.nextCurrentShapeY = 0

    def redraw(self, x, y, number, s):
        self.gridMatrix = deepcopy(self.gridMatrixCopy)
        stateX = 1
        stateY = 1
        dimension = self.dico[number][self.currentShape][-1]
        for i in range(y, y + dimension[1]):
            for j in range(int(len(self.gridMatrix[i]))):
                if j >= x and stateX <= dimension[0]:
                    if self.dico[number][s][stateY - 1][stateX - 1] != 0:
                        self.gridMatrix[i][j] = self.dico[number][s][stateY - 1][stateX - 1]
                    stateX += 1
            stateX = 1
            stateY += 1

    def rapid_move_left(self):
        if not self.gameOver:
            self.currentShapeX -= 1
            if self.currentShapeX < 0:
                self.currentShapeX = 0
            self.bricks_collision(self.currentShapeX, self.currentShapeY, self.currentNumber, self.currentShape, 1)
            self.collideLeft = False
            self.redraw(self.currentShapeX, self.currentShapeY, self.currentNumber, self.currentShape)

    def rotate(self):
        self.currentShape += 1
        if self.currentShape >= len(self.dico[self.currentNumber]):
            self.currentShape = 0
        self.right_side_gate()
        if self.bricks_collision_rotation(self.currentShapeX, self.currentShapeY, self.currentNumber,
                                          self.currentShape):
            self.currentShape -= 1
        self.redraw(self.currentShapeX, self.currentShapeY, self.currentNumber, self.currentShape)

    def rapid_move_right(self):
        if not self.gameOver:
            self.currentShapeX += 1
            self.right_side_gate()
            self.bricks_collision(self.currentShapeX, self.currentShapeY, self.currentNumber, self.currentShape, -1)
            self.collideLeft = False
            self.redraw(self.currentShapeX, self.currentShapeY, self.currentNumber, self.currentShape)

    def rapid_move(self):
        if not self.buttonLeftRelease:
            if time() - self.startTime2 >= 0.5:
                self.rapid_move_left()
        if not self.buttonRightRelease:
            if time() - self.startTime2 >= 0.5:
                self.rapid_move_right()

    def right_side_gate(self):
        if (self.dico[self.currentNumber][self.currentShape][-1][0] + self.currentShapeX) * 20 > self.resolution[0]:
            self.currentShapeX = int(self.resolution[0] / 20) - self.dico[self.currentNumber][self.currentShape][-1][0]

    def bottom_side_gate(self):
        if (self.dico[self.currentNumber][self.currentShape][-1][1] + self.currentShapeY) * 20 >= self.resolution[1]:
            self.add_falled_bricks()

    def add_falled_bricks(self):
        self.gridMatrixCopy = deepcopy(self.gridMatrix)
        self.complete_line()
        self.choose_shape()

    def complete_line(self):
        case = 0
        self.lines.clear()
        for i in range(len(self.gridMatrix)):
            for j in range(len(self.gridMatrix[i])):
                if self.gridMatrix[i][j] != 0:
                    case += 1
            if case == int(self.resolution[0] / 20):
                self.numberOfLineCompleted += 1
                self.lines.append(i)
            case = 0
        if len(self.lines) != 0:
            for i in self.lines:
                for j in range(len(self.gridMatrixCopy[i])):
                    self.gridMatrixCopy[i][j] = 0
                for k in reversed(range(len(self.gridMatrixCopy))):
                    if k <= i and k != 0:
                        self.gridMatrixCopy[k] = deepcopy(self.gridMatrixCopy[k - 1])
                self.score += 100
                self.scoreFontRender = self.hardFont.render(str(self.score), True, 'white')

    def collision(self, x, y, number, s):
        stateX = 1
        stateY = 1
        dimension = self.dico[number][self.currentShape][-1]
        for i in range(y, y + dimension[1]):
            for j in range(int(len(self.gridMatrix[i]))):
                if j >= x and stateX <= dimension[0]:
                    if self.dico[number][s][stateY - 1][stateX - 1] != 0:
                        for k in range(len(self.gridMatrixCopy)):
                            for l in range(int(len(self.gridMatrixCopy[0]))):
                                if self.gridMatrixCopy[k][l] != 0 and not self.collide:
                                    if j == l and (i + 1) * 20 == k * 20:
                                        if self.currentShapeY <= 0:
                                            self.gameOver = True
                                        if not self.gameOver:
                                            self.add_falled_bricks()
                                            self.collide = True
                                        else:
                                            self.game_over()
                    stateX += 1
            stateX = 1
            stateY += 1

    def bricks_collision(self, x, y, number, s, v):
        stateX = 1
        stateY = 1
        dimension = self.dico[number][self.currentShape][-1]
        for i in range(y, y + dimension[1]):
            for j in range(int(len(self.gridMatrix[i]))):
                if j >= x and stateX <= dimension[0]:
                    if self.dico[number][s][stateY - 1][stateX - 1] != 0:
                        for k in range(len(self.gridMatrixCopy)):
                            for l in range(int(len(self.gridMatrixCopy[0]))):
                                if self.gridMatrixCopy[k][l] != 0 and not self.collideLeft:
                                    if pygame.Rect((j * 20, i * 20, 20, 20)).colliderect(
                                            pygame.Rect((l * 20, k * 20, 20, 20))):
                                        self.currentShapeX = self.currentShapeX + v
                                        self.collideLeft = True
                    stateX += 1
            stateX = 1
            stateY += 1

    def bricks_collision_rotation(self, x, y, number, s):
        stateX = 1
        stateY = 1
        dimension = self.dico[number][self.currentShape][-1]
        for i in range(y, y + dimension[1]):
            for j in range(int(len(self.gridMatrix[i]))):
                if j >= x and stateX <= dimension[0]:
                    if self.dico[number][s][stateY - 1][stateX - 1] != 0:
                        for k in range(len(self.gridMatrixCopy)):
                            for l in range(int(len(self.gridMatrixCopy[0]))):
                                if self.gridMatrixCopy[k][l] != 0 and not self.collideLeft:
                                    if pygame.Rect((j * 20, i * 20, 20, 20)).colliderect(
                                            pygame.Rect((l * 20, k * 20, 20, 20))):
                                        self.collideLeft = True
                                        return True
                    stateX += 1
            stateX = 1
            stateY += 1

    def auto_fall(self):
        self.currentShapeY += 1 * self.vitesse
        self.redraw(self.currentShapeX, self.currentShapeY, self.currentNumber, self.currentShape)

    def game_over(self):
        self.isGamePaused = False
        self.startPlaying = True
        self.update_best_score()

    def replay(self):
        self.gridMatrix.clear()
        self.gridMatrixCopy.clear()
        self.grid_matrix_filler()
        self.choose_shape()
        self.score = 0
        self.scoreFontRender = self.hardFont.render(str(self.score), True, 'white')
        self.read_best_score()
        self.gameOver = False

    def draw_help(self):
        board = pygame.Rect((50, 50, 400, 500))
        y = board.y + 20
        pygame.draw.rect(self.window, "blue", (48, 48, 404, 504), width=2)
        pygame.draw.rect(self.window, "black", board)
        for render in self.helpMessageFontRenderList:
            self.window.blit(render, (board.x + 20, y))
            y += 20

    def init_game(self):
        self.grid_matrix_filler()
        self.nextCurrentNumber = random.randint(1, 5)
        self.nextColor = random.randint(1, 8)
        self.nextCurrentShape = 0
        self.nextCurrentShapeX = random.randint(0, int(self.resolution[0] / 20) - 2)
        self.nextCurrentShapeY = 0
        self.redraw(self.nextCurrentShapeX, self.nextCurrentShapeY, self.nextCurrentNumber, self.nextCurrentShape)
        self.choose_shape()


if __name__ == "__main__":
    Tetris((500, 600)).main()
