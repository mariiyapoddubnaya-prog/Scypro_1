import math


def square(side):
    area = side * side
    return math.ceil(area)


# Пример проверки (можно удалить или оставить)
print(square(2.5))  # 2.5 * 2.5 = 6.25 -> округление вверх даст 7