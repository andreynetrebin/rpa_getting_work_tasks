import logging
from config import load_config
from logger import setup_logging
from web_driver import WebDriverManager
from data_extractor import DataExtractor
from excel_handler import ExcelHandler

def main():
    """Основная функция для выполнения RPA скрипта."""
    setup_logging()  # Настраиваем логирование
    url, user_login, user_password = load_config()
    
    logging.info(f'Запуск под учетной записью - {user_login}')  # Логируем начало работы скрипта
    
    # Инициализация WebDriver
    driver_manager = WebDriverManager()
    driver = driver_manager.initialize_driver()
    
    try:
        driver_manager.login(driver, url, user_login, user_password)  # Авторизация в приложении
        data_extractor = DataExtractor(driver)
        
        # Извлечение данных и сохранение в Excel
        data_53_12_1, data_53_13 = data_extractor.extract_data()
        ExcelHandler.insert_to_xlsx('53_12_1.xlsx', data_53_12_1)
        ExcelHandler.insert_to_xlsx('53_13.xlsx', data_53_13)

    except Exception as e:
        logging.error(f'Возникла ошибка: {e}')  # Логируем ошибки
    finally:
        driver.quit()  # Закрываем драйвер
        logging.info('Работа скрипт завершена!')  # Логируем завершение работы скрипта

if __name__ == "__main__":
    main()  # Запускаем основную функцию
