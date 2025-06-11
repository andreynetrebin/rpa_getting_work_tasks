import logging
from os import path, makedirs, getcwd

def setup_logging():
    """Настраивает конфигурацию логирования."""
    work_directory = getcwd()
    logs_directory = path.join(work_directory, 'logs')
    if not path.exists(logs_directory):  # Если директория не существует
        makedirs(logs_directory)  # Создаем директорию

    log_filename = f'{path.basename(__file__).split(".")[0]}.log'  # Формируем имя файла лога
    logging.basicConfig(
        format='%(levelname)-8s [%(asctime)s] %(message)s',
        level=logging.INFO,
        filename=path.join(logs_directory, log_filename)  # Указываем путь к файлу лога
    )
