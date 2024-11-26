from assembler import assembler, serializer, log_operation

# Тестирование функции assembler

def test_load():
    print("Running test_load()...")
    bytes = assembler([{"operation": "load", "args": [539]}])
    assert bytes == [0xB8, 0x21, 0x00, 0x00, 0x00], f"Test failed: {bytes}"  # Проверяем ожидаемый бинарный результат
    print("test_load passed!")

def test_read():
    print("Running test_read()...")
    bytes = assembler([{"operation": "read", "args": [163]}])
    assert bytes == [0x34, 0x0A, 0x00], f"Test failed: {bytes}"  # Проверяем ожидаемый бинарный результат
    print("test_read passed!")

def test_write():
    print("Running test_write()...")
    bytes = assembler([{"operation": "write", "args": [671]}])
    assert bytes == [0xFD, 0x29, 0x00], f"Test failed: {bytes}"  # Проверяем ожидаемый бинарный результат
    print("test_write passed!")

def test_abs():
    print("Running test_abs()...")
    bytes = assembler([{"operation": "abs", "args": []}])
    assert bytes == [0x00], f"Test failed: {bytes}"  # Проверяем ожидаемый бинарный результат
    print("test_abs passed!")

# Тестирование функции serializer

def test_serializer_load():
    print("Running test_serializer_load()...")
    cmd = 8
    fields = [(539, 4)]
    size = 5
    bytes = serializer(cmd, fields, size)
    assert bytes == b'\xB8\x21\x00\x00\x00', f"Test failed: {bytes}"  # Проверяем ожидаемый бинарный результат
    print("test_serializer_load passed!")

def test_serializer_read():
    print("Running test_serializer_read()...")
    cmd = 4
    fields = [(163, 4)]
    size = 3
    bytes = serializer(cmd, fields, size)
    assert bytes == b'\x34\x0A\x00', f"Test failed: {bytes}"  # Проверяем ожидаемый бинарный результат
    print("test_serializer_read passed!")

def test_serializer_write():
    print("Running test_serializer_write()...")
    cmd = 13
    fields = [(671, 4)]
    size = 3
    bytes = serializer(cmd, fields, size)
    assert bytes == b'\xFD\x29\x00', f"Test failed: {bytes}"  # Проверяем ожидаемый бинарный результат
    print("test_serializer_write passed!")

def test_serializer_abs():
    print("Running test_serializer_abs()...")
    cmd = 0
    fields = []
    size = 1
    bytes = serializer(cmd, fields, size)
    assert bytes == b'\x00', f"Test failed: {bytes}"  # Проверяем ожидаемый бинарный результат
    print("test_serializer_abs passed!")

# Тестирование логирования операций

def test_log_operation():
    print("Running test_log_operation()...")
    log_file = "log.csv"
    
    # Проверка для команды load (A=8, B=539)
    log_operation(log_file, 8, 539)
    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        assert lines[-1] == "A=8,B=539\n", f"Test failed: {lines[-1]}"
    
    # Проверка для команды read (A=4, B=163)
    log_operation(log_file, 4, 163)
    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        assert lines[-1] == "A=4,B=163\n", f"Test failed: {lines[-1]}"

    print("test_log_operation passed!")

# Тестирование комбинации инструкций

def test_multiple_instructions():
    print("Running test_multiple_instructions()...")
    instructions = [
        {"operation": "load", "args": [539]},  # Загрузка константы (A=8, B=539)
        {"operation": "read", "args": [163]},  # Чтение из памяти (A=4, B=163)
        {"operation": "write", "args": [671]},  # Запись в память (A=13, B=671)
        {"operation": "abs", "args": []}  # Унарная операция abs() (A=0)
    ]
    bytes = assembler(instructions)
    expected_bytes = [
        0xB8, 0x21, 0x00, 0x00, 0x00,  # load 539
        0x34, 0x0A, 0x00,  # read 163
        0xFD, 0x29, 0x00,  # write 671
        0x00  # abs
    ]
    assert bytes == expected_bytes, f"Test failed: {bytes}"  # Проверяем, что последовательность байтов совпадает
    print("test_multiple_instructions passed!")

# Запуск всех тестов вручную
def run_tests():
    test_load()
    test_read()
    test_write()
    test_abs()
    test_serializer_load()
    test_serializer_read()
    test_serializer_write()
    test_serializer_abs()
    test_log_operation()
    test_multiple_instructions()
    print("All tests passed successfully!")

if __name__ == "__main__":
    run_tests()
