from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from characters import Character


class Item:
    """
    Класс для игровых предметов, которые могут применять различные эффекты к персонажам.
    Эффекты: лечение, усиление атаки, усиление защиты.
    """
    def __init__(self, name: str, effect_type: str, value: int) -> None:
        """
        Инициализация предмета.

        :param name: Название предмета
        :param effect_type: Тип эффекта ('heal', 'boost_attack', 'boost_defense')
        :param value: Значение эффекта (насколько увеличивается параметр)
        """
        self.name = name
        self.effect_type = effect_type  # heal, boost_attack, boost_defense
        self.value = value

    def apply(self, target: 'Character') -> None:
        """
        Применяет эффект предмета к персонажу.

        :param target: Персонаж, к которому применяется предмет
        """
        if self.effect_type == 'heal':
            old_health = target.health
            target.health += self.value
            print(f"{target.name} восстановил {self.value} здоровья. Здоровье: {old_health} -> {target.health}")
        elif self.effect_type == 'boost_attack':
            old_attack = target.attack_power
            target.attack_power += self.value
            print(f"{target.name} увеличил атаку на {self.value}. Атака: {old_attack} -> {target.attack_power}")
        elif self.effect_type == 'boost_defense':
            old_defense = target.defense
            target.defense += self.value
            print(f"{target.name} увеличил защиту на {self.value}. Защита: {old_defense} -> {target.defense}")

    def __str__(self) -> str:
        """
        Строковое представление предмета, включает его эффект.

        :return: Строка с описанием предмета и его эффекта
        """
        effect_descriptions = {
            'heal': f"восстанавливает {self.value} здоровья",
            'boost_attack': f"увеличивает атаку на {self.value}",
            'boost_defense': f"увеличивает защиту на {self.value}"
        }
        return  f"{self.name} ({effect_descriptions.get(self.effect_type, 'неизвестный эффект')})"