from abc import ABC, abstractmethod
import pygame
import Service
import random


class AbstractObject(ABC):
    def draw(self, display):
        pass


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


class Interactive(ABC):
    @abstractmethod
    def interact(self, engine, hero):
        pass


class Ally(AbstractObject, Interactive):
    def __init__(self, icon, action, position):
        self.sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        self.action(engine, hero)


class Creature(AbstractObject):
    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.max_hp = None
        self.calc_max_hp()
        self.hp = self.max_hp
        self.screen_x = 0
        self.screen_y = 0

    def calc_max_hp(self):
        self.max_hp = 5 + self.stats["endurance"] * 2

    def set_screen_pos(self, min_x, min_y):
        self.screen_x = self.position[0] - min_x
        self.screen_y = self.position[1] - min_y

    def draw(self, display):
        rect = self.sprite.get_rect()
        display.blit(self.sprite, (rect.width * self.screen_x, rect.width * self.screen_y))


class Hero(Creature):
    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 100
        super().__init__(icon, stats, pos)

    def level_up(self):
        ups = []
        while self.exp >= 100 * (2 ** (self.level - 1)):
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_hp()
            self.hp = self.max_hp
            ups.append("Level up!")
        return ups


class Enemy(Creature, Interactive):
    def __init__(self, icon, stats, xp, position):
        super().__init__(icon, stats, position)     # TODO
        self.xp = xp
        self.action = Service.fight_against_hero

    def interact(self, engine, hero):
        self.action(self, engine, hero)


class Effect(Hero):
    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.position = base.position
        self.hp = base.hp
        self.max_hp = base.max_hp
        self.exp = base.exp
        self.level = base.level
        self.apply_effect()

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @sprite.setter
    def sprite(self, value):
        self.base.sprite = value

    @abstractmethod
    def apply_effect(self):
        pass


class Berserk(Effect):
    def apply_effect(self):
        self.stats['strength'] += 5


class Blessing(Effect):
    def apply_effect(self):
        self.stats['strength'] += 2
        self.stats['luck'] += 2
        self.stats['endurance'] += 2


class Weakness(Effect):
    def apply_effect(self):
        self.stats['strength'] -= 1
        self.stats['luck'] -= 2


class Fortune(Effect):
    def apply_effect(self):
        self.stats['luck'] += 5
