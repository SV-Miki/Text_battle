import random
from typing import List

import constants
from items import Item


class Character:
    """
    Базовый класс для всех персонажей (игрок и враги).
    Содержит основные характеристики и методы боя.
    """

    def __init__(self, name: str, health: int, attack: int, defense: int) -> None:
        """
        Инициализация персонажа.
        :param name: Имя персонажа.
        :param health: Количество здоровья.
        :param attack: Сила атаки.
        :param defense: Защита.
        """
        self.name = name
        self.health = health
        self.attack_power = attack
        self.defense = defense

    def attack(self, target: "Character") -> None:
        """
        Атакует другого персонажа.
        :param target: Персонаж, по которому атакуют.
        """
        damage = max(
            constants.MIN_DAMAGE, self.attack_power - target.defense
        )  # Урон не может быть меньше 1.
        print(f"{self.name} атакует {target.name}")
        target.take_damage(damage)
        print(f"{self.name} наносит {damage} урона {target.name}")

    def take_damage(self, amount: int) -> None:
        """
        Получить урон.
        :param amount: Количество урона.
        """
        self.health -= amount
        print(f"{self.name} получает {amount} урона. Осталось {self.health} здоровья")

    def is_alive(self) -> bool:
        """Проверяет, жив ли персонаж."""
        return self.health > 0

    def describe(self) -> None:
        """Выводит характеристики персонажа."""
        print(
            f"{self.name} | Здоровье: {self.health}, Атака: {self.attack_power}, Защита: {self.defense}"
        )


class Player(Character):
    """
    Класс игрока. Расширяет Character, добавляя инвентарь, опыт и уровни.
    """

    def __init__(
        self,
        name: str,
        health: int = constants.PLAYER_BASE_HEALTH,
        attack: int = constants.PLAYER_BASE_ATTACK,
        defense: int = constants.PLAYER_BASE_DEFENSE,
        exp: int = constants.PLAYER_BASE_EXP,
        level: int = constants.PLAYER_BASE_LEVEL,
    ) -> None:
        super().__init__(name, health, attack, defense)
        self._inventory: List[Item] = []
        self._exp = exp
        self._level = level

    def add_item(self, item: Item) -> None:
        """
        Добавляет предмет в инвентарь.
        :param item: Добавляемый предмет.
        """
        self._inventory.append(item)
        print(f"{self.name} получил предмет: {item}")

    def use_item(self, item_index: int) -> None:
        """
        Применяет предмет из инвентаря по индексу.
        :param item_index: Индекс предмета в инвентаре.
        """
        try:
            item = self._inventory[item_index]
            item.apply(self)
            self._inventory.pop(item_index)
        except IndexError:
            print("Неверный индекс предмета")

    def show_inventory(self) -> None:
        """Выводит список предметов в инвентаре."""
        if not self._inventory:
            print("Инвентарь пуст")
            return
        print("\n=== Инвентарь ===")
        for i, item in enumerate(self._inventory):
            print(f"{i + 1}. {item}")

    def gain_exp(self, amount: int) -> None:
        """
        Получение опыта игроком.
        :param amount: Количество опыта.
        """
        self._exp += amount
        print(f"{self.name} получил {amount} опыта. Всего: {self._exp}")

        exp_for_next_level = self._level * constants.EXP_PER_LEVEL
        if self._exp >= exp_for_next_level:
            self.level_up()

    def level_up(self) -> None:
        """Повышает уровень игрока и увеличивает характеристики."""
        self._level += 1
        self.health += constants.HEALTH_INCREMENT
        self.attack_power += constants.ATTACK_INCREMENT
        self.defense += constants.DEFENSE_INCREMENT
        print(f"{self.name} достиг уровня {self._level}.")
        print(
            f"Здоровье +{constants.HEALTH_INCREMENT}, Атака +{constants.ATTACK_INCREMENT}, Защита +{constants.DEFENSE_INCREMENT}"
        )
        print(
            f"Новые характеристики. Здоровье: {self.health}, Атака: {self.attack_power}, Защита: {self.defense}"
        )

    def describe(self) -> None:
        """Выводит расширенное описание игрока с уровнем и опытом."""
        super().describe()
        print(
            f"Уровень: {self._level}, Опыт: {self._exp}/{self._level * constants.EXP_PER_LEVEL}"
        )


class Enemy(Character):
    """
    Базовый класс врага, расширяет Character.
    Содержит награду за победу.
    """

    def __init__(
        self,
        name: str,
        health: int,
        attack: int,
        defense: int,
        exp_reward: int,
        taunts: List[str],
    ) -> None:
        """
        Инициализация врага.
        :param name: Имя врага.
        :param health: Здоровье.
        :param attack: Атака.
        :param defense: Защита.
        :param exp_reward: Опыт за победу.
        :param taunts: Список боевых реплик.
        """
        super().__init__(name, health, attack, defense)
        self.exp_reward = exp_reward  # Количество опыта за победу над врагом
        self.taunts = taunts

    def get_taunt(self) -> str:
        """Возвращает боевую реплику врага."""
        if not self.taunts:
            return "..."
        return random.choice(self.taunts)


class Goblin(Enemy):
    """
    Класс для врага - гоблина.
    """

    def __init__(self) -> None:
        """Инициализация гоблина с фиксированными параметрами."""
        super().__init__(
            name=self.__class__.__name__,
            health=constants.GOBLIN_HEALTH,
            attack=constants.GOBLIN_ATTACK,
            defense=constants.GOBLIN_DEFENSE,
            exp_reward=constants.GOBLIN_EXP_REWARD,
            taunts=constants.GOBLIN_TAUNTS,
        )


class Troll(Enemy):
    """
    Класс для врага - тролля.
    """

    def __init__(self) -> None:
        """Инициализация тролля с фиксированными параметрами."""
        super().__init__(
            name=self.__class__.__name__,
            health=constants.TROLL_HEALTH,
            attack=constants.TROLL_ATTACK,
            defense=constants.TROLL_DEFENSE,
            exp_reward=constants.TROLL_EXP_REWARD,
            taunts=constants.TROLL_TAUNTS,
        )


class Dragon(Enemy):
    """
    Класс для врага - дракона.
    """

    def __init__(self) -> None:
        """Инициализация дракона с фиксированными параметрами."""
        super().__init__(
            name=self.__class__.__name__,
            health=constants.DRAGON_HEALTH,
            attack=constants.DRAGON_ATTACK,
            defense=constants.DRAGON_DEFENSE,
            exp_reward=constants.DRAGON_EXP_REWARD,
            taunts=constants.DRAGON_TAUNTS,
        )
