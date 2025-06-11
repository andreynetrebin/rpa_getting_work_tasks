from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import logging
import time

class WebDriverManager:
    """Класс для управления WebDriver."""

    def __init__(self):
        self.service = Service(executable_path='driver/chromedriver.exe')

    def initialize_driver(self):
        """Инициализирует Chrome WebDriver."""
        options = Options()
        options.add_argument("--headless")  # Запускаем браузер в фоновом режиме
        driver = webdriver.Chrome(service=self.service, options=options)
        return driver

    def login(self, driver, url, user_login, user_password):
        """Выполняет вход в веб-приложение."""
        driver.get(url)  # Открываем URL
        time.sleep(5)
        logging.info("Открыта главная страница")

        driver.find_element(By.ID, "username").send_keys(user_login)  # Вводим логин
        driver.find_element(By.ID, "password").send_keys(user_password)  # Вводим пароль

        login_button = driver.find_element(By.XPATH, "/html/body/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/form/div/button")
        login_button.click()  # Нажимаем кнопку входа
        time.sleep(3)  # Ждем 3 секунды
        logging.info("Успешно выполнен вход")
