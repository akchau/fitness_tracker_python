class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(
            self,
            training_type: str,
            duration: float,
            distance: float,
            speed: float,
            calories: float) -> str:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> None:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            round(self.duration, 3),
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        return ((18
                * self.get_mean_speed()
                - 20)
                * self.weight
                / self.M_IN_KM
                * self.duration
                * 60)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((0.035
                * self.weight
                + (self.get_mean_speed()
                    ** 2
                    // self.height)
                * 0.029
                * self.weight)
                * self.duration
                * 60)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            length_pool: float,
            count_pool: float):
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.lenght_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + 1.1) * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    try:
        if workout_type == "SWM":
            return Swimming(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4])
        elif workout_type == "RUN":
            return Running(data[0], data[1], data[2])
        elif workout_type == "WLK":
            return SportsWalking(data[0], data[1], data[2], data[3])
    except IndexError:
        print('Ошибка чтения данных с датчиков')


def main(training: Training) -> None:
    """Главная функция."""
    try:
        message_train = training.show_training_info()
        print(message_train.get_message())
    except AttributeError:
        print('Данный тип тренировки неизвестен')
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('WRK', [9000, 1, 75, 180]),  # передаем невалидный код тренировки
        ('WLK', [0, 1, 75, 180]),  # передаем нулевое значение движений
        ([9000, 1, 75, 180]),  # не передаем тип тренировки
        ('WLK', [1, 75, 180])  # передаем неправильное количество параметров

    ]
    for i in range(len(packages)):
        if len(packages[i]) == 2:
            workout_type = packages[i][0]
            data = packages[i][1]
            if packages[i][1][0] > 0:
                training = read_package(workout_type, data)
                main(training)
            else:
                print('Вы еще не начали тренироваться=)')
        else:
            print('Не определен тип тренировки или датчики неисправны')
