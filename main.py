import logging
from config import load_config
from logger import setup_logging
from web_driver import WebDriverManager
from data_extractor import DataExtractor
from excel_handler import ExcelHandler


def main():
    """Основная функция для выполнения RPA скрипта."""
    setup_logging()  # Настраиваем логирование
    url, user_login, user_password, classification_codes = load_config()

    logging.info(f'Запуск под учетной записью - {user_login}')  # Логируем начало работы скрипта
    logging.info(f'Используемые коды классификаций: {", ".join(classification_codes)}')  # Логируем коды классификаций

    # Инициализация WebDriver
    driver_manager = WebDriverManager()
    driver = driver_manager.initialize_driver()

    try:
        driver_manager.login(driver, url, user_login, user_password)  # Авторизация в приложении
        data_extractor = DataExtractor(driver, classification_codes)  # Передаем драйвер и классификации

        # Извлечение данных и сохранение в Excel
        data_dict = data_extractor.extract_data()  # Получаем словарь с данными
        for code, data in data_dict.items():
            ExcelHandler.insert_to_xlsx(f'{code}.xlsx', data)  # Сохраняем данные в Excel

    except Exception as e:
        logging.error(f'Возникла ошибка: {e}')  # Логируем ошибки
    finally:
        driver.quit()  # Закрываем драйвер
        logging.info('Работа скрипта завершена!')  # Логируем завершение работы скрипта


if __name__ == "__main__":
    main()  # Запускаем основную функцию