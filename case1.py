def sum_min_max_arr():
  # Печатаем сообщение, просящее пользователя ввести элементы массива
  print('Введите элементы массива через пробел: ')

  # Читаем ввод пользователя, разделяем его по пробелам и преобразуем каждый элемент в целое число
  arr = list(map(int, input().split()))

  # Находим минимальный и максимальный элементы массива
  arr_min = min(arr)
  arr_max = max(arr)

  # Находим индексы минимального и максимального элементов
  arr_min_index = arr.index(arr_min)
  arr_max_index = arr.index(arr_max)

  # Печатаем минимальный и максимальный элементы, а также их индексы
  print(
      f"MIN: {arr_min}, MAX: {arr_max}, MININ: {arr_min_index}, MAXIN: {arr_max_index}"
  )

  # Если индекс минимального элемента больше индекса максимального, меняем их местами
  if arr_min_index > arr_max_index:
    arr_min_index, arr_max_index = arr_max_index, arr_min_index

  # Инициализируем переменную для суммы отрицательных элементов
  summa = 0

  # Проходим по элементам массива между минимальным и максимальным
  for i in arr[arr_min_index + 1:arr_max_index]:
    # Если элемент отрицательный, добавляем его к сумме
    if i < 0:
      summa += i

  # Возвращаем сумму отрицательных элементов
  return summa


# Вызываем функцию sum_min_max_arr() и печатаем результат
if __name__ == "__main__":
  print(
      f'Сумма отрицательных элементов между минимальным и максимальным элементом: {sum_min_max_arr()}'
  )
'''
Введите элементы массива через пробел: 
1 2 3 4 40 -2 -2 -40
MIN: -40, MAX: 40, MININ: 7, MAXIN: 4
Сумма отрицательных элементов между минимальным и максимальным элементом: -4

Введите элементы массива через пробел: 
1 2 3 4 -40 -2 -2 40
MIN: -40, MAX: 40, MININ: 4, MAXIN: 7
Сумма отрицательных элементов между минимальным и максимальным элементом: -4
'''
