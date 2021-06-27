from abc import ABC, abstractmethod

'''
class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []
        self.stats = {
            "HP": 128,  # health points
            "MP": 42,  # magic points,
            "SP": 100,  # skill points
            "Strength": 15,  # сила
            "Perception": 4,  # восприятие
            "Endurance": 8,  # выносливость
            "Charisma": 2,  # харизма
            "Intelligence": 3,  # интеллект
            "Agility": 8,  # ловкость
            "Luck": 1  # удача
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()
'''


class AbstractEffect(Hero, ABC):
    def __init__(self, base):
        self.base = base

    @abstractmethod
    def get_positive_effects(self):
        raise NotImplementedError

    @abstractmethod
    def get_negative_effects(self):
        raise NotImplementedError


class AbstractPositive(AbstractEffect):
    @abstractmethod
    def get_positive_effects(self):
        raise NotImplementedError

    def get_negative_effects(self):
        return self.base.get_negative_effects()


class AbstractNegative(AbstractEffect):
    @abstractmethod
    def get_negative_effects(self):
        raise NotImplementedError

    def get_positive_effects(self):
        return self.base.get_positive_effects()


# POSITIVE
class Berserk(AbstractPositive):
    def get_positive_effects(self):
        base_positive = self.base.get_positive_effects()
        current_positive = base_positive + ['Berserk']
        return current_positive

    def get_stats(self):
        base_stats = self.base.get_stats()
        for k in base_stats:
            if k in ["Perception", "Charisma", "Intelligence"]:
                base_stats[k] -= 3
            elif k in ["Strength", "Endurance", "Agility", "Luck"]:
                base_stats[k] += 7
            elif k in ["HP"]:
                base_stats[k] += 50
        return base_stats


class Blessing(AbstractPositive):
    def get_positive_effects(self):
        base_positive = self.base.get_positive_effects()
        current_positive = base_positive + ['Blessing']
        return current_positive

    def get_stats(self):
        base_stats = self.base.get_stats()
        for k in base_stats:
            if k in ["Perception", "Charisma", "Intelligence", "Strength", "Endurance", "Agility", "Luck"]:
                base_stats[k] += 2
        return base_stats


# NEGATIVE
class Weakness(AbstractNegative):
    def get_negative_effects(self):
        base_negative = self.base.get_negative_effects()
        current_negative = base_negative + ['Weakness']
        return current_negative

    def get_stats(self):
        base_stats = self.base.get_stats()
        for k in base_stats:
            if k in ["Strength", "Endurance", "Agility"]:
                base_stats[k] -= 4
        return base_stats


class EvilEye(AbstractNegative):
    def get_negative_effects(self):
        base_negative = self.base.get_negative_effects()
        current_negative = base_negative + ['EvilEye']
        return current_negative

    def get_stats(self):
        base_stats = self.base.get_stats()
        for k in base_stats:
            if k in ["Luck"]:
                base_stats[k] -= 10
        return base_stats


class Curse(AbstractNegative):
    def get_negative_effects(self):
        base_negative = self.base.get_negative_effects()
        current_negative = base_negative + ['Curse']
        return current_negative

    def get_stats(self):
        base_stats = self.base.get_stats()
        for k in base_stats:
            if k in ["Perception", "Charisma", "Intelligence", "Strength", "Endurance", "Agility", "Luck"]:
                base_stats[k] -= 2
        return base_stats
