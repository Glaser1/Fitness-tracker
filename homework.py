from typing import Type, Optional


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str, duration: int, distance: float, speed: float, calories: float) -> None:
        self.training_type: str = training_type
        self.duration: int = duration
        self.distance: float = distance
        self.speed: float = speed
        self.calories: float = calories

    def get_message(self) -> str:
        return (
            f"Тип тренировки: {self.training_type}; Длительность: {self.duration:0.3f} ч.; "
            f"Дистанция: {self.distance:0.3f} км; Ср. скорость: {self.speed:0.3f} км/ч; "
            f"Потрачено ккал: {self.calories:0.3f}."
        )


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    TIME_CONST: float = 60

    def __init__(
        self,
        action: int,
        duration: int,
        weight: float,
    ) -> None:
        self.action: int = action
        self.duration: int = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / (self.duration)

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )

    def __str__(self):
        return f"{self.action}, {self.duration}, {self.weight}"


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self, action, duration, weight) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> Optional[float]:
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.TIME_CONST
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029
    KM_S_TO_M_S: float = 0.278
    SM_TO_M: int = 100

    def __init__(self, action: int, duration: int, weight: int, height: int) -> None:
        super().__init__(action, duration, weight)
        self.height: int = height

    def get_spent_calories(self) -> Optional[float]:
        return (
            (
                self.COEFF_CALORIE_1 * self.weight
                + (
                    (self.get_mean_speed() * self.KM_S_TO_M_S) ** 2
                    / (self.height / self.SM_TO_M)
                )
                * self.COEFF_CALORIE_2
                * self.weight
            )
            * self.duration
            * self.TIME_CONST
        )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    MEAN_SPEED_SHIFT: float = 1.1
    SPEED_MULTIPLIER: int = 2

    def __init__(self, action: int, duration: int, weight: int, length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> Optional[float]:
        return (
            (self.get_mean_speed() + self.MEAN_SPEED_SHIFT)
            * self.SPEED_MULTIPLIER
            * self.weight
            * self.duration
        )

    def __str__(self) -> str:
        return f"{self.action}, {self.duration}, {self.weight}, {self.length_pool}, {self.count_pool}"


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные, полученные от датчиков."""
    workout_classes_mapping: dict[str, Type[Training]] = {"SWM": Swimming, "RUN": Running, "WLK": SportsWalking}
    return workout_classes_mapping[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages: list = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
