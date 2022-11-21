from typing import Dict, Type

LEN_STEP = 0.65
M_IN_KM = 1000
LEN_STEP = 0.65
LEN_STROKE = 1.38
CALORIES_MEAN_SPEED_MULTIPLIER = 18
CALORIES_MEAN_SPEED_SHIFT = 1.79


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str, duration: int, distance: float,
                 speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        print(
            f'Тип тренировки: {self.training_type}; Длительность: '
            f'{self.duration} ч.; Дистанция: {self.distance:.2f} км; Ср. '
            f'скорость: {self.speed:.2f} км/ч; Потрачено ккал: '
            f'{self.calories:.2f}.')


class Training:
    """Базовый класс тренировки."""
    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * LEN_STEP / M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self):
        return (
            CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed() +
            CALORIES_MEAN_SPEED_SHIFT) * self.weight / M_IN_KM *\
            self.duration * 60


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        calories = (self.get_mean_speed() * 1000/3600)**2 / self.height / 100
        calories = calories + 0.035 * self.weight
        return calories * 0.029 * self.weight * self.duration * 60


class Swimming(Training):
    """Тренировка: плавание."""
    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.length_pool * self.count_pool / M_IN_KM

    def get_spent_calories(self):
        return (self.get_mean_speed() + 1.1) * 2 * self.weight * self.duration


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return training_type[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    info.get_message()


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
