import configparser

def load_config():
    """Загружает учетные данные пользователя из файла конфигурации."""
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    return config.get('web_address', 'url'), config.get('user', 'login'), config.get('user', 'password')
