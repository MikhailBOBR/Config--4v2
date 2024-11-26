import argparse
from assembler import assembler, save_to_bin
from interpreter import interpreter

def generate_abs_instructions(vector):
    """
    Генерирует инструкции для применения операции abs() к каждому элементу вектора.
    Результат записывается обратно в тот же вектор.
    """
    instructions = []

    for i in range(len(vector)):
        # Применяем abs() к элементу вектора
        abs_value = abs(vector[i])

        # Записываем абсолютное значение в стек
        instructions.append({
            "operation": "load",  # Операция загрузки
            "args": [abs_value]    # Загружаем абсолютное значение в стек
        })
        
        # Применяем abs() (хотя оно уже применено)
        instructions.append({
            "operation": "abs",  # Операция abs()
            "args": []            # Применяем abs()
        })
        
        # Записываем результат обратно в память по индексу i
        instructions.append({
            "operation": "write",  # Операция записи
            "args": [i]            # Записываем результат обратно в вектор по индексу i
        })

    return instructions


def main():
    # Параметры файлов
    binary_file = "test_binary.bin"
    result_file = "test_result.xml"  # Файл для записи результата
    log_file = "test_log.csv"

    # Генерация инструкций
    vector = [-5, 10, -15, 20, -25]
    instructions = generate_abs_instructions(vector)

    # Сохраняем их в бинарный файл через ассемблер
    save_to_bin(assembler(instructions, log_file), binary_file)

    # Запускаем интерпретатор для выполнения
    interpreter(binary_file, result_file, (0, len(vector) - 1))

if __name__ == "__main__":
    main()
