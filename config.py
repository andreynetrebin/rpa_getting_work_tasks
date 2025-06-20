import configparser

def load_config():
    """Загружает учетные данные пользователя и коды классификаций из файла конфигурации."""
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    url = config.get('web_address', 'url')
    user_login = config.get('user', 'login')
    user_password = config.get('user', 'password')
    classification_codes = config.get('classifications', 'codes').split(',')  # Загружаем коды классификаций
    classification_codes = [code.strip() for code in classification_codes]  # Убираем пробелы
    return url, user_login, user_password, classification_codes