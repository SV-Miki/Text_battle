import json
import random
from typing import List, Tuple, Type

import constants
from characters import Dragon, Enemy, Goblin, Player, Troll
from items import EffectType, Item

ENEMY_TYPES_WITH_WEIGHTS: List[Tuple[Type[Enemy], int]] = [
    (Goblin, 60),
    (Troll, 30),
    (Dragon, 10),
]
ENEMY_POPULATION = [enemy_type[0] for enemy_type in ENEMY_TYPES_WITH_WEIGHTS]
ENEMY_WEIGHTS = [enemy_type[1] for enemy_type in ENEMY_TYPES_WITH_WEIGHTS]

AVAILABLE_ITEMS = [
    Item("Зелье лечения", EffectType.HEAL, 20),
    Item("Элексир силы", EffectType.BOOST_ATTACK, 5),
    Item("Свиток защиты", EffectType.BOOST_DEFENSE, 3),
    Item("Большое зелье лечения", EffectType.HEAL, 40),
    Item("Мощный эликсир силы", EffectType.BOOST_ATTACK, 8),
    Item("Мощный свиток защиты", EffectType.BOOST_DEFENSE, 5),
]


def spawn_enemy() -> Enemy:
    """Случайным образом создаёт и возвращает противника: 60% гоблин, 30% тролль, 10% дракон."""
    chosen_enemy_class = random.choices(ENEMY_POPULATION, weights=ENEMY_WEIGHTS, k=1)[0]
    return chosen_enemy_class()


def get_random_item() -> Item:
    """Случайным образом выбирает и возвращает предмет."""
    return random.choice(AVAILABLE_ITEMS)


def save_game(player: Player) -> None:
    """
    Сохраняет состояние игрока в файл save_game.json.
    Включает основные характеристики и инвентарь.
    """
    save_data = {
        "name": player.name,
        "health": player.health,
        "attack": player.attack_power,
        "defense": player.defense,
        "exp": player._exp,
        "level": player._level,
        "inventory": [
            {
                "name": item.name,
                "effect_type": item.effect_type.value,
                "value": item.value,
            }
            for item in player._inventory
        ],
    }

    # Сохраняем JSON в файл с кодировкой UTF-8
    with open("save_game.json", "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=4)

    print("Игра сохранена")


def load_game() -> Player | None:
    """
    Загружает состояние игрока из файла save_game.json.
    В случае неудачи возвращает None.
    """
    try:
        # Чтение данных из файла
        with open("save_game.json", "r", encoding="utf-8") as f:
            save_data = json.load(f)

        # Восстановление игрока и его характеристик
        player = Player(
            name=save_data["name"],
            health=save_data["health"],
            attack=save_data["attack"],
            defense=save_data["defense"],
            exp=save_data["exp"],
            level=save_data["level"],
        )
        # Восстановление инвентаря из списка предметов
        for item_data in save_data["inventory"]:
            player.add_item(
                Item(
                    name=item_data["name"],
                    effect_type=EffectType(item_data["effect_type"]),
                    value=item_data["value"],
                )
            )

        print(f"Игра загружена для персонажа {player.name}")
        return player
    except (FileNotFoundError, json.JSONDecodeError):
        print("Сохранение не найдено")
        return None


def main_menu() -> Player | None:
    """
    Основное меню игры: выбор нового персонажа, загрузка или выход.
    Возвращает объект игрока или None (если выход).
    """
    while True:
        print("\n===Текстовая боёвка===")
        print("1. Новая игра")
        print("2. Загрузить игру")
        print("3. Выйти")

        choice = input("> ")

        if choice == "1":
            name = input("Введите имя героя: ")
            return Player(name=name, exp=0, level=1)
        elif choice == "2":
            loaded_player = load_game()
            if loaded_player:
                return loaded_player
        elif choice == "3":
            return None
        else:
            print("Неверный выбор. Попробуйте снова")


class GameLoop:
    """Класс для управления игровым циклом, хранит player и enemy."""

    def __init__(self, player: Player) -> None:
        self.player = player
        self.enemy = spawn_enemy()

    def handle_attack(self) -> None:
        """Обрабатывает действие атаки."""
        self.player.attack(self.enemy)
        if self.enemy.is_alive():
            self.enemy.attack(self.player)

    def handle_use_item(self) -> None:
        """Обрабатывает действие использования предмета."""
        if not self.player._inventory:
            print("Инвентарь пуст")
            return

        self.player.show_inventory()
        item_choice = input("Выберите предмет (номер) или 0 для отмены: ").strip()
        if item_choice == "0":
            return

        try:
            item_index = int(item_choice) - 1
        except ValueError:
            print("Некорректный ввод. Введите число.")
            return

        # Проверка индекса и использование предмета
        if 0 <= item_index < len(self.player._inventory):
            self.player.use_item(item_index)
            if self.enemy.is_alive():  # Если мы все еще в бою
                self.enemy.attack(self.player)
        else:
            print("Неверный номер предмета.")

    def handle_show_inventory(self) -> None:
        """Обрабатывает действие просмотра инвентаря."""
        self.player.show_inventory()

    def handle_show_status(self) -> None:
        """Обрабатывает действие показа статуса."""
        print("\n=== Статус персонажей ===")
        self.player.describe()
        self.enemy.describe()

    def handle_save_game(self) -> None:
        """Обрабатывает действие сохранения игры."""
        save_game(self.player)

    def handle_exit_game(self) -> None:
        """Обрабатывает выход из игры."""
        print("Выход из игры. До новых встреч.")
        exit()

    def run(self) -> None:
        """
        Главный игровой цикл. Управляет ходом игры: меню, бой, инвентарь, сохранение и окончание.
        """
        print(f"\nДобро пожаловать, {self.player.name}")
        print("Приключение начинается\n")

        # Если у игрока пустой инвентарь — даём стартовый предмет
        if not self.player._inventory:
            self.player.add_item(Item("Зелье лечения", EffectType.HEAL, 20))

        actions = {
            "1": self.handle_attack,
            "2": self.handle_use_item,
            "3": self.handle_show_inventory,
            "4": self.handle_show_status,
            "5": self.handle_save_game,
            "6": self.handle_exit_game,
        }
        # Основной цикл — пока игрок жив
        while self.player.is_alive():
            print(f"\nВы встретили {self.enemy.name}")
            print(f"{self.enemy.name}: '{self.enemy.get_taunt()}'")

            battle_active = True

            # Цикл сражения с одним противником
            while battle_active and self.player.is_alive() and self.enemy.is_alive():
                print("\nВаши действия:")
                print("1. Атаковать")
                print("2. Использовать предмет")
                print("3. Посмотреть инвентарь")
                print("4. Показать статус")
                print("5. Сохранить игру")
                print("6. Выйти из игры")

                choice = input("> ")

                if handler := actions.get(choice):
                    handler()
                else:
                    print("Неверный выбор. Попробуйте снова")

                # Проверяем — побеждён ли враг
                if not self.enemy.is_alive():
                    print(f"\nВы победили {self.enemy.name}")
                    self.player.gain_exp(self.enemy.exp_reward)

                    # Шанс получить случайный предмет
                    if random.random() < constants.ITEM_DROP_CHANCE:  # 70% шанс
                        item = get_random_item()
                        self.player.add_item(item)

                    self.enemy = spawn_enemy()
                    battle_active = False

        # Если вышли из цикла — игрок погиб
        print("\n=== ИГРА ОКОНЧЕНА ===")
        print(f"{self.player.name} пал в бою.")
        print(f"Итоговый уровень: {self.player._level}")
        print(f"Накоплено опыта: {self.player._exp}")


def game_loop() -> None:
    """Запуск игрового цикла."""
    player = main_menu()
    if not player:
        return

    game = GameLoop(player)
    game.run()


# Точка входа: запуск игры при старте файла
if __name__ == "__main__":
    game_loop()
