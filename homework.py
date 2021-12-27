from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE = ('Тип тренировки: {}; '
               'Длительность: {:.3f} ч.; '
               'Дистанция: {:.3f} км; '
               'Ср. скорость: {:.3f} км/ч; '
               'Потрачено ккал: {:.3f}.')

    def get_message(self) -> None:
        t = asdict(self)
        return self.MESSAGE.format(*t.values())


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_H: int = 60

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
        raise NotImplementedError(
            'Определите get_spent_calories в %s.' %
            (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    first_coef: int = 18
    second_coef: int = 20

    def get_spent_calories(self) -> float:
        return ((self.first_coef
                * self.get_mean_speed()
                - self.second_coef)
                * self.weight
                / self.M_IN_KM
                * self.duration
                * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    first_coef: float = 0.035
    second_coef: int = 2
    thrid_coef: float = 0.029

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.first_coef
                * self.weight
                + (self.get_mean_speed()
                    ** self.second_coef
                    // self.height)
                * self.thrid_coef
                * self.weight)
                * self.duration
                * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    first_coef: float = 1.1
    second_coef: int = 2

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
        return (
            (self.get_mean_speed()
                + self.first_coef)
            * self.second_coef
            * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    parameters_train = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    if workout_type in parameters_train:
        return parameters_train[workout_type](*data)
    else:
        pass


def main(training: Training) -> None:
    """Главная функция."""
    try:
        message_train = training.show_training_info()
        print(message_train.get_message())
    except AttributeError:
        print('Данный тип тренировки неизвестен')


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
                try:
                    training = read_package(workout_type, data)
                except TypeError:
                    pass
                try:
                    main(training)
                except ZeroDivisionError:
                    print('Ошибка датчиков')
            else:
                print('Вы еще не начали тренироваться=)')
        else:
            print('Не определен тип тренировки или датчики неисправны')
