#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Добавлены возможности:
    - Отображение нескольких кривых одновременно (максимум 9)
        нажмите клавишу 1-9, чтобы начать добавлять опорные точки
        в соответствующую кривую. Номер текущей активной кривой
        показан внизу экрана

    - Удаление опорной точки: нажмите клавишу "D", затем выберите
        точку для удаления

    - Усорение и замедление движения кривых: нажмите "W" или "S"
        для ускорения и замедления соответственно
"""

import pygame
import random


SCREEN_W = 800
SCREEN_H = 600
SCREEN_DIM = (SCREEN_W, SCREEN_H)
VERTEX_POINT_WIDTH = 7
KNOT_POINT_WIDTH = 3
KNOT_COUNT = 9

game_speed = 1
steps = 10
current_knot_num = 0
digit_keys = {i: i - 49 for i in range(49, 58)}


def len(obj):
    if isinstance(obj, Vec2d):
        return obj.length()
    return obj.__len__()


class Vec2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_under_mouse = False

    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y)

    def __mul__(self, k):
        return Vec2d(k * self.x, k * self.y)

    def length(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def int_pair(self):
        return int(self.x), int(self.y)

    def draw(self, color, width):
        pygame.draw.circle(gameDisplay, color, self.int_pair(), width)

    def draw_line_to(self, other, color, width):
        pygame.draw.line(gameDisplay, color, self.int_pair(), other.int_pair(), width)

    def check_mouse(self):
        x, y = pygame.mouse.get_pos()
        if (x - self.x) ** 2 + (y - self.y) ** 2 < VERTEX_POINT_WIDTH ** 2:
            self.is_under_mouse = True
        else:
            self.is_under_mouse = False


class MovingPoint(Vec2d):
    def __init__(self, x, y, vx, vy):
        super().__init__(x, y)
        self.velocity = Vec2d(vx, vy)

    def move(self):
        new_coord = self + self.velocity * game_speed
        self.x, self.y = new_coord.x, new_coord.y
        self.check_borders()

    def check_borders(self):
        if self.x > SCREEN_W or self.x < 0:
            self.velocity.x = -self.velocity.x
        if self.y > SCREEN_H or self.y < 0:
            self.velocity.y = -self.velocity.y


class Polyline:
    def __init__(self):
        self.points = list()

    def add_point(self, coordinates: tuple):
        vx, vy = random.random() * 2, random.random() * 2
        new_point = MovingPoint(*coordinates, vx, vy)
        self.points.append(new_point)

    def delete_point(self):
        for i in range(len(self.points)):
            if self.points[i].is_under_mouse:
                del self.points[i]
                break

    def set_points(self):
        for p in self.points:
            p.move()

    def draw_points(self, style="points", width=VERTEX_POINT_WIDTH, color=(255, 255, 255), points=None):
        """функция отрисовки точек на экране"""
        points = points or self.points
        if style == "line":
            for i in range(-1, len(points) - 1):
                points[i].draw_line_to(points[i + 1], color, width)

        elif style == "points":
            for p in points:
                if p.is_under_mouse:
                    p.draw((255, 0, 0), width + 4)
                p.draw(color, width)

    def clear_points(self):
        self.points = list()

    def check_mouse_for_points(self):
        for p in self.points:
            p.check_mouse()


class Knot(Polyline):
    def __init__(self):
        super().__init__()
        self.knot_points = list()

    def add_point(self, coordinates: tuple):
        super().add_point(coordinates)
        self.get_knot(steps)

    def delete_point(self):
        super().delete_point()
        self.get_knot(steps)

    def set_points(self):
        super().set_points()
        self.get_knot(steps)

    def get_knot(self, count):
        res = []
        if len(self.points) > 2:
            for i in range(-2, len(self.points) - 2):
                ptn = list()
                ptn.append((self.points[i + 0] + self.points[i + 1]) * 0.5)
                ptn.append(self.points[i + 1])
                ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)
                res.extend(self.get_points(ptn, count))
        self.knot_points = res

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def draw_knot_points(self, style="line", width=KNOT_POINT_WIDTH, color=(255, 255, 255)):
        self.get_knot(steps)
        if len(self.knot_points) >= 3:
            super().draw_points(style, width, color, self.knot_points)

    def clear_points(self):
        super().clear_points()
        self.knot_points = list()


def draw_help():
    """функция отрисовки экрана справки программы"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = [["F1", "Show Help"],
            ["R", "Restart"],
            ["P", "Pause/Play"],
            ["D", "Delete Point"],
            ["1-9", "Activate knot 1-9"],
            ["Num+", "More points"],
            ["Num-", "Less points"],
            ["", ""],
            ["", f"Current points: {steps}"]
            ]

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


def draw_delete_tip():
    font = pygame.font.SysFont("serif", 34)
    data = "Choose point to delete"
    gameDisplay.blit(font.render(data, True, (200, 0, 0)), (60, 40))


def draw_current_knot_num():
    font = pygame.font.SysFont("serif", 14)
    gameDisplay.blit(font.render("current active knot: " + str(current_knot_num + 1), True, (100, 100, 100)), (20, SCREEN_H - 20))


def game_main_loop():
    global game_speed
    global current_knot_num
    global steps
    working = True
    show_help = False
    pause = True
    delete_mode = False
    hue = 0
    main_color = pygame.Color(0)
    knots = [Knot() for i in range(KNOT_COUNT)]
    knot = knots[current_knot_num]

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    for k in knots:
                        k.clear_points()
                if event.key == pygame.K_p:
                    pause = not pause
                    delete_mode = False
                if event.key == pygame.K_d:
                    delete_mode = not delete_mode
                    pause = True
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                    delete_mode = False
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                if event.key == pygame.K_s:
                    game_speed = max(0, game_speed - 0.2)
                if event.key == pygame.K_w:
                    game_speed = min(5, game_speed + 0.2)
                if event.key in digit_keys:
                    current_knot_num = digit_keys[event.key]
                    knot = knots[current_knot_num]

            if event.type == pygame.MOUSEBUTTONDOWN:
                if delete_mode:
                    for k in knots:
                        k.delete_point()
                else:
                    knot.add_point(event.pos)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 0.1) % 360
        main_color.hsla = (hue, 100, 50)

        for k in knots:
            k.draw_points()
            k.draw_knot_points(color=main_color)
            if not pause:
                k.set_points()
            if delete_mode:
                k.check_mouse_for_points()
        if show_help:
            draw_help()
        if delete_mode:
            draw_delete_tip()

        draw_current_knot_num()
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    game_main_loop()
    pygame.display.quit()
    pygame.quit()
    exit(0)
