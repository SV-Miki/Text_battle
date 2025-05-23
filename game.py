from typing import Optional
from characters import Player, Enemy, Goblin, Troll, Dragon
from items import Item
import json
import random


def spawn_enemy() -> Enemy:
    """Случайным образом создаёт и возвращает противника: 60% гоблин, 30% тролль, 10% дракон."""
    roll = random.random()
    if roll < 0.6:  #60% шанс
        return Goblin()
    elif roll < 0.9:  #30% шанс
        return Troll()
    else:
        return Dragon()

def get_random_item() -> Item:
    """Случайным образом выбирает и возвращает предмет."""
    items = [
        Item("Зелье лечения", "heal", 20),
        Item("Элексир силы", "boost_attack", 5),
        Item("Свиток защиты", "boost_defense", 3),
        Item("Большое зелье лечения", "heal", 40),
        Item("Мощный эликсир силы", "boost_attack", 8),
        Item("Мощный свиток защиты", "boost_defense", 5)
    ]
    return random.choice(items)

def save_game(player: Player) -> None:
    """
    Сохраняет состояние игрока в файл save_game.json.
    Включает основные характеристики и инвентарь.
    """
    save_data = {
        'name': player.name,
        'health': player.health,
        'attack': player.attack_power,
        'defense': player.defense,
        'exp': player.exp,
        'level': player.level,
        'inventory': [
            {'name': item.name, 'effect_type': item.effect_type, 'value': item.value}
            for item in player.inventory
        ]
    }

    # Сохраняем JSON в файл с кодировкой UTF-8
    with open('save_game.json', 'w', encoding='utf-8') as f:
        json.dump(save_data, f, ensure_ascii=False, indent=4)

    print("Игра сохранена")


def load_game() -> Optional[Player]:
    """
    Загружает состояние игрока из файла save_game.json.
    В случае неудачи возвращает None.
    """
    try:
        # Чтение данных из файла
        with open('save_game.json', 'r', encoding='utf-8') as f:
            save_data = json.load(f)

        # Восстановление игрока и его характеристик
        player = Player(
        name=save_data['name'],
        health=save_data['health'],
        attack=save_data['attack'],
        defense=save_data['defense']
        )
        player.exp = save_data['exp']
        player.level = save_data['level']

        # Восстановление инвентаря из списка предметов
        for item_data in save_data['inventory']:
            player.add_item(Item(
                name=item_data['name'],
                effect_type=item_data['effect_type'],
                value=item_data['value']
            ))

        print(f"Игра загружена для персонажа {player.name}")
        return player
    except (FileNotFoundError, json.JSONDecodeError):
        print("Сохранение не найдено")
        return None


def main_menu() -> Optional[Player]:
    """
    Основное меню игры: выбор нового персонажа, загрузка или выход.
    Возвращает объект игрока или None (если выход).
    """
    print("\n===Текстовая боёвка===")
    print("1. Новая игра")
    print("2. Загрузить игру")
    print("3. Выйти")

    choice = input("> ")

    if choice == "1":
        name = input("Введите имя героя: ")
        return Player(name)
    elif choice == "2":
        return load_game()
    elif choice == "3":
        return None
    else:
        print("Неверный выбор. Попробуйте снова")
        return main_menu()


def game_loop() -> None:
    """
    Главный игровой цикл. Управляет ходом игры: меню, бой, инвентарь, сохранение и окончание.
    """
    player = main_menu()
    if not player:
        return

    print(f"\nДобро пожаловать, {player.name}")
    print("Приключение начинается\n")

    # Если у игрока пустой инвентарь — даём стартовый предмет
    if not player.inventory:
        player.add_item(Item("Зелье лечения", "heal", 20))

    enemy = spawn_enemy()

    # Основной цикл — пока игрок жив
    while player.is_alive():
        print(f"\nВы встретили {enemy.name}")
        print(f"{enemy.name}: '{enemy.get_taunt()}'")

        battle_active = True

        # Цикл сражения с одним противником
        while battle_active and player.is_alive() and enemy.is_alive():
            print("\nВаши действия:")
            print("1. Атаковать")
            print("2. Использовать предмет")
            print("3. Посмотреть инвентарь")
            print("4. Показать статус")
            print("5. Сохранить игру")
            print("6. Выйти из игры")

            choice = input("> ")

            if choice == "1":
                player.attack(enemy)
                if enemy.is_alive():
                    enemy.attack(player)

            elif choice == "2":
                # Показываем игроку инвентарь и даём выбрать предмет
                player.show_inventory()
                if player.inventory:
                    try:
                        item_index = int(input("Выберите предмет (номер) или 0 для отмены: ")) - 1
                        if item_index >= 0:
                            player.use_item(item_index)
                            if enemy.is_alive():
                                enemy.attack(player)
                    except ValueError:
                        print("Введите число")

            elif choice == "3":
                # Просмотр инвентаря
                player.show_inventory()

            elif choice == "4":
                # Показ информации о герое и враге
                print("\n=== Статус персонажей ===")
                player.describe()
                enemy.describe()

            elif choice == "5":
                # Сохраняем игру
                save_game(player)

            elif choice == "6":
                # Выход из игры
                print("Выход из игры. До новых встреч.")
                exit()

            else:
                print("Неверный выбор. Попробуйте снова")

            # Проверяем — побеждён ли враг
            if not  enemy.is_alive():
                print(f"\nВы победили {enemy.name}")
                player.gain_exp(enemy.exp_reward)

                # Шанс получить случайный предмет
                if random.random() < 0.7:   # 70% шанс
                    item = get_random_item()
                    player.add_item(item)

                enemy = spawn_enemy()
                battle_active = False

    # Если вышли из цикла — игрок погиб
    print("\n=== ИГРА ОКОНЧЕНА ===")
    print(f"{player.name} пал в бою.")
    print(f"Итоговый уровень: {player.level}")
    print(f"Накоплено опыта: {player.exp}")

# Точка входа: запуск игры при старте файла
if __name__ == "__main__":
    game_loop()