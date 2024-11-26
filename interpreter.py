import argparse
import struct
import xml.etree.ElementTree as ET
from xml.dom import minidom

def popcnt(value):
    """Подсчет количества установленных битов (единиц) в числе."""
    return bin(value).count('1')

def interpreter(binary_path, result_path, memory_range):
    # Инициализация памяти УВМ и регистров
    memory = [0] * 256  # Пусть у нас будет 256 ячеек памяти
    stack = []  # Используем стек для хранения значений
    registers = [0] * 16  # 16 регистров
    
    # Инициализация памяти с тестовыми значениями
    # Например, загружаем в память значения для проверки
    memory[6] = 100  # Для адреса 6 положим значение 100
    memory[7] = 200  # Для адреса 7 положим значение 200

    # Чтение бинарного файла
    with open(binary_path, "rb") as f:
        byte_code = f.read()

    i = 0  # Указатель на текущую команду
    while i < len(byte_code):
        # Извлечение команды из первых 4 битов
        command = byte_code[i] & 0x0F
        print(f"Шаг {i}: Команда 0x{command:X}")
        
        if command == 8:  # Загрузка константы
            B = struct.unpack("<I", byte_code[i+1:i+5])[0]  # Получаем значение константы из 4 байт
            stack.append(B)
            print(f"Загружена константа {B} в стек")
            i += 5
        elif command == 4:  # Чтение из памяти
            B = (byte_code[i] >> 4) & 0x0F  # Адрес регистра
            address = struct.unpack("<H", byte_code[i+1:i+3])[0]  # Адрес в памяти
            registers[B] = memory[address]
            print(f"Прочитано значение {memory[address]} из памяти по адресу {address} в регистр {B}")
            i += 3
        elif command == 13:  # Запись в память
            B = (byte_code[i] >> 4) & 0x0F  # Адрес регистра
            address = struct.unpack("<H", byte_code[i+1:i+3])[0]  # Адрес в памяти
            memory[address] = registers[B]  # Записываем значение регистра в память
            registers[B] = 0  # Обнуляем регистр после записи
            print(f"Записано значение {memory[address]} из регистра {B} в память по адресу {address}")
            # Логирование состояния памяти
            print(f"Состояние памяти на шаге {i}: {memory[:32]}")  # Печатаем первые 32 ячейки памяти для наглядности
            i += 3
        elif command == 0:  # Унарная операция abs()
            if stack:  # Проверка, что в стеке есть хотя бы один элемент
                B = stack.pop()  # Извлекаем элемент из стека
                stack.append(abs(B))  # Применяем абсциссу и возвращаем обратно в стек
                print(f"Применена операция abs() к значению {B}, результат: {abs(B)}")
            else:
                print("Ошибка: Стек пуст при попытке выполнить операцию abs()")
            i += 1
        else:
            raise ValueError(f"Неизвестная команда: {command}")

    # Запись результатов в XML файл
    root = ET.Element("memory")
    for address in range(memory_range[0], memory_range[1] + 1):
        memory_element = ET.SubElement(root, "memory_element", address=str(address))
        memory_element.text = str(memory[address])

    # Форматирование XML для читаемого вида
    xml_str = ET.tostring(root, encoding="utf-8")
    parsed_str = minidom.parseString(xml_str)  # Преобразуем в объект DOM для отступов
    pretty_xml_str = parsed_str.toprettyxml(indent="  ")  # Форматируем строку с отступами

    # Запись отформатированного XML в файл
    with open(result_path, "w", encoding="utf-8") as result_file:
        result_file.write(pretty_xml_str)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Интерпретатор для выполнения инструкций из бинарного файла.")
    parser.add_argument("binary_path", help="Путь к бинарному файлу")
    parser.add_argument("result_path", help="Путь к XML-файлу для результатов")
    parser.add_argument("first_index", type=int, help="Первый индекс диапазона памяти")
    parser.add_argument("last_index", type=int, help="Последний индекс диапазона памяти")
    args = parser.parse_args()
    
    interpreter(args.binary_path, args.result_path, (args.first_index, args.last_index))
