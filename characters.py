from typing import List
from items import Item
import random


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

    def attack(self, target: 'Character') -> None:
        """
        Атакует другого персонажа.
        :param target: Персонаж, по которому атакуют.
        """
        damage = max(1, self.attack_power - target.defense) # Урон не может быть меньше 1.
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
        print(f"{self.name} | Здоровье: {self.health}, Атака: {self.attack_power}, Защита: {self.defense}")


class Player(Character):
    """
    Класс игрока. Расширяет Character, добавляя инвентарь, опыт и уровни.
    """
    def __init__(self, name: str, health: int = 100, attack: int = 10, defense: int = 5) -> None:
        super().__init__(name, health, attack, defense)
        self.inventory: List[Item] = []
        self.exp = 0
        self.level = 1

    def add_item(self, item: Item) -> None:
        """
        Добавляет предмет в инвентарь.
        :param item: Добавляемый предмет.
        """
        self.inventory.append(item)
        print(f"{self.name} получил предмет: {item}")

    def use_item(self, item_index: int) -> None:
        """
        Применяет предмет из инвентаря по индексу.
        :param item_index: Индекс предмета в инвентаре.
        """
        if 0 <= item_index < len(self.inventory):
            item = self.inventory[item_index]
            item.apply(self)
            self.inventory.pop(item_index)
        else:
            print("Неверный индекс предмета")

    def show_inventory(self) -> None:
        """Выводит список предметов в инвентаре."""
        if not self.inventory:
            print("Инвентарь пуст")
            return
        print("\n=== Инвентарь ===")
        for i, item in enumerate(self.inventory):
            print(f"{i+1}. {item}")

    def gain_exp(self, amount: int) -> None:
        """
        Получение опыта игроком.
        :param amount: Количество опыта.
        """
        self.exp += amount
        print(f"{self.name} получил {amount} опыта. Всего: {self.exp}")

        exp_for_next_level = self.level * 100
        if self.exp >= exp_for_next_level:
            self.level_up()

    def level_up(self) -> None:
        """Повышает уровень игрока и увеличивает характеристики."""
        self.level += 1
        self.health += 20
        self.attack_power += 5
        self.defense += 3
        print(f"{self.name} достиг уровня {self.level}.")
        print("Здоровье +20, Атака +5, Защита +3")
        print(f"Новые характеристики. Здоровье: {self.health}, Атака: {self.attack_power}, Защита: {self.defense}")

    def describe(self) -> None:
        """Выводит расширенное описание игрока с уровнем и опытом."""
        super().describe()
        print(f"Уровень: {self.level}, Опыт: {self.exp}/{self.level * 100}")


class Enemy(Character):
    """
    Базовый класс врага, расширяет Character.
    Содержит награду за победу.
    """
    def __init__(self, name: str, health: int, attack: int, defense: int, exp_reward: int) -> None:
        """
        Инициализация врага.
        :param name: Имя врага.
        :param health: Здоровье.
        :param attack: Атака.
        :param defense: Защита.
        :param exp_reward: Опыт за победу.
        """
        super().__init__(name, health, attack, defense)
        self.exp_reward = exp_reward    #Количество опыта за победу над врагом

    def get_taunt(self) -> str:
        """Возвращает боевую реплику врага."""
        return "..."

class Goblin(Enemy):
    """
    Класс для врага - гоблина.
    """
    def __init__(self) -> None:
        """Инициализация гоблина с фиксированными параметрами."""
        super().__init__("Goblin", health=30, attack=7, defense=2, exp_reward=20)

    def get_taunt(self) -> str:
        """Возвращает случайную угрозу."""
        taunts = [
            "Я украду твои вещи!",
            "Еще один глупый искатель приключений!"
        ]
        return random.choice(taunts)


class Troll(Enemy):
    """
    Класс для врага - тролля.
    """
    def __init__(self) -> None:
        """Инициализация тролля с фиксированными параметрами."""
        super().__init__("Troll", health=70, attack=12, defense=6, exp_reward=50)

    def get_taunt(self) -> str:
        """Возвращает случайную угрозу."""
        taunts = [
            "Я раздавлю тебя!",
            "Ты слишком мал для меня!"
        ]
        return random.choice(taunts)


class Dragon(Enemy):
    """
    Класс для врага - дракона.
    """
    def __init__(self) -> None:
        """Инициализация дракона с фиксированными параметрами."""
        super().__init__("Dragon", health=150, attack=20, defense=10, exp_reward=150)

    def get_taunt(self) -> str:
        """Возвращает случайную угрозу."""
        taunts = [
            "Ты осмелился потревожить мой сон?",
            "Ты не уйдешь отсюда живым!"
        ]
        return random.choice(taunts)