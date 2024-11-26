import argparse
import struct
import xml.etree.ElementTree as ET

# Функция для сериализации команд в бинарный формат
def serializer(cmd, fields, size):
    bits = 0
    bits |= cmd
    for value, offset in fields:
        bits |= (value << offset)
    return bits.to_bytes(size, "little")

# Функция для логирования операций в файл
def log_operation(log_path, operation_code, *args):
    if log_path is not None:
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(f"A={operation_code}")
            if args:  # Если аргументы существуют
                log_file.write(f",B={args[0]}")
                if len(args) > 1:
                    log_file.write(f",C={args[1]}")
            log_file.write("\n")

# Основной ассемблер
def assembler(instructions, log_path=None):
    byte_code = []
    for instruction in instructions:
        operation = instruction['operation']
        args = instruction['args']

        if operation == "load":
            # Загрузка константы
            B = args[0]  # Константа
            byte_code += serializer(8, [(B, 4)], 5)
            log_operation(log_path, 8, B)

        elif operation == "read":
            # Чтение из памяти
            B = args[0]  # Адрес
            byte_code += serializer(4, [(B, 4)], 3)
            log_operation(log_path, 4, B)

        elif operation == "write":
            # Запись в память
            B = args[0]  # Адрес
            byte_code += serializer(13, [(B, 4)], 3)
            log_operation(log_path, 13, B)

        elif operation == "abs":
            # Унарная операция abs()
            byte_code += serializer(0, [], 1)
            log_operation(log_path, 0)

    return byte_code

# Чтение XML и преобразование в инструкции
def parse_input_xml(input_xml_path):
    tree = ET.parse(input_xml_path)
    root = tree.getroot()

    instructions = []
    for instruction in root.findall('instruction'):
        operation = instruction.find('operation').text
        args = [int(arg.text) for arg in instruction.findall('arg')]
        instructions.append({'operation': operation, 'args': args})
    
    return instructions

# Сохранение ассемблированных инструкций в бинарный файл
def save_to_bin(assembled_instructions, binary_path):
    with open(binary_path, "wb") as binary_file:
        binary_file.write(bytes(assembled_instructions))

# Основная точка входа
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assembling the instructions from XML to byte-code.")
    parser.add_argument("input_xml_path", help="Path to the input XML file")
    parser.add_argument("binary_path", help="Path to the binary file (bin)")
    parser.add_argument("log_path", help="Path to the log file (csv)")
    args = parser.parse_args()

    # Инициализируем файл лога
    with open(args.log_path, "w", encoding="utf-8") as log_file:
        log_file.write(f"Operation code,Constant/Address\n")

    # Парсим XML и ассемблируем
    instructions = parse_input_xml(args.input_xml_path)
    result = assembler(instructions, args.log_path)

    # Сохраняем бинарный файл
    save_to_bin(result, args.binary_path)
