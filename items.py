from enum import Enum
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from characters import Character


class EffectType(Enum):
    HEAL = "heal"
    BOOST_ATTACK = "boost_attack"
    BOOST_DEFENSE = "boost_defense"


class Item:
    """
    Класс для игровых предметов, которые могут применять различные эффекты к персонажам.
    Эффекты: лечение, усиление атаки, усиление защиты.
    """

    # Константы класса для описаний эффектов
    EFFECT_DESCRIPTIONS = {
        EffectType.HEAL: "восстанавливает {} здоровья",
        EffectType.BOOST_ATTACK: "увеличивает атаку на {}",
        EffectType.BOOST_DEFENSE: "увеличивает защиту на {}",
    }

    # _effect_handlers - это словарь,
    # где ключи - это EffectType, а значения - функции,
    # которые принимают Character и возвращают None.
    _effect_handlers: dict[EffectType, Callable[["Character"], None]]

    def __init__(self, name: str, effect_type: EffectType, value: int) -> None:
        """
        Инициализация предмета.

        :param name: Название предмета
        :param effect_type: Тип эффекта (EffectType.HEAL, EffectType.BOOST_ATTACK, EffectType.BOOST_DEFENSE)
        :param value: Значение эффекта (насколько увеличивается параметр)
        """
        self.name = name
        self.effect_type = effect_type  # EffectType
        self.value = value
        self._effect_handlers = {
            EffectType.HEAL: self._apply_heal,
            EffectType.BOOST_ATTACK: self._apply_boost_attack,
            EffectType.BOOST_DEFENSE: self._apply_boost_defense,
        }

    def _apply_heal(self, target: "Character") -> None:
        """Применяет эффект лечения."""
        old_health = target.health
        target.health += self.value
        print(
            f"{target.name} восстановил {self.value} здоровья. Здоровье: {old_health} -> {target.health}"
        )

    def _apply_boost_attack(self, target: "Character") -> None:
        """Применяет эффект усиления атаки."""
        old_attack = target.attack_power
        target.attack_power += self.value
        print(
            f"{target.name} увеличил атаку на {self.value}. Атака: {old_attack} -> {target.attack_power}"
        )

    def _apply_boost_defense(self, target: "Character") -> None:
        """Применяет эффект усиления защиты."""
        old_defense = target.defense
        target.defense += self.value
        print(
            f"{target.name} увеличил защиту на {self.value}. Защита: {old_defense} -> {target.defense}"
        )

    def apply(self, target: "Character") -> None:
        """
        Применяет эффект предмета к персонажу.

        :param target: Персонаж, к которому применяется предмет
        """
        if handler := self._effect_handlers.get(self.effect_type):
            handler(target)
        else:
            print(f"Неизвестный эффект для предмета {self.name}")

    def __str__(self) -> str:
        """
        Строковое представление предмета, включает его эффект.

        :return: Строка с описанием предмета и его эффекта
        """
        description_template = self.EFFECT_DESCRIPTIONS.get(
            self.effect_type, "неизвестный эффект"
        )
        if description_template != "неизвестный эффект":
            description = description_template.format(self.value)
        else:
            description = description_template
        return f"{self.name} ({description})"
