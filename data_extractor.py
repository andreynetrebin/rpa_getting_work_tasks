from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import logging
import math
import time
from selenium.webdriver import ActionChains
from work_task_accepter import WorkTaskAccepter


class DataExtractor:
    """Класс для извлечения данных из веб-приложения."""

    def __init__(self, driver, classification_codes):
        """Инициализирует экземпляр класса DataExtractor."""
        self.driver = driver
        self.classification_codes = classification_codes  # Инициализируем коды классификаций

    def extract_data(self):
        """Извлекает релевантные данные из веб-приложения."""
        self.login_and_navigate()  # Выполняем вход и переходим к нужной странице
        quantity_records = self.get_quantity_records()  # Получаем общее количество записей

        data_dict = {code: [] for code in self.classification_codes}  # Инициализируем словарь для данных

        for _ in range(math.ceil(quantity_records / 20)):  # Итерируемся по страницам данных
            html = self.driver.page_source
            data_from_html = self.get_data_from_html(html)

            for code in self.classification_codes:
                data_dict[code].extend(data_from_html.get(code, []))  # Добавляем данные в соответствующий список

            if _ < math.ceil(quantity_records / 20) - 1:
                self.click_next_page()  # Переходим на следующую страницу

        logging.info(f"Всего получено строк: {sum(len(data) for data in data_dict.values())}")
        work_tasks = [work_task[0] for data in data_dict.values() for work_task in data]

        # Используем WorkTaskAccepter для принятия рабочих заданий
        task_accepter = WorkTaskAccepter(self.driver)
        task_accepter.accept_work_tasks(work_tasks)

        return data_dict  # Возвращаем словарь с данными

    # Остальной код DataExtractor остается без изменений
    def login_and_navigate(self):
        """Выполняет вход в приложение и переходит к разделу 'Рабочие задания'."""
        self.navigate_to_work_tasks()
        self.hover_over_work_tasks()

    def navigate_to_work_tasks(self):
        """Переходит к разделу 'Рабочие задания'."""
        action = ActionChains(self.driver)
        element = WebDriverWait(self.driver, 45).until(
            EC.presence_of_element_located((By.XPATH,
                                            "/html/body/form/div/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td[1]/div/table/tbody/tr/td/div/div[2]/div[1]/div[2]/div/ul/li[7]"))
        )
        action.move_to_element(element).perform()

        work_tasks = WebDriverWait(self.driver, 45).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mea59820d_ns_menu_WO_MODULE_sub_changeapp_WOTRACK_a"))
        )
        work_tasks.click()
        time.sleep(15)
        logging.info("Перешли в Рабочие задания")

    def hover_over_work_tasks(self):
        """Наводит курсор на элемент меню 'Рабочие задания'."""
        # Ждем, пока элемент с номером класса станет доступным
        number_cls = WebDriverWait(self.driver, 45).until(
            EC.presence_of_element_located((By.XPATH,
                                            "/html/body/form/div/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td[3]/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[2]/td[9]/input"))
        )

        # Формируем строку с кодами классификаций
        classification_input = ','.join([f"={code}" for code in self.classification_codes])

        # Вводим коды классификаций
        number_cls.send_keys(classification_input)
        time.sleep(1)

        # Ждем, пока элемент со статусом станет доступным
        status = WebDriverWait(self.driver, 45).until(
            EC.presence_of_element_located((By.XPATH,
                                            "/html/body/form/div/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td[3]/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[2]/td[13]/input"))
        )

        # Устанавливаем статус
        status.send_keys("=Назначено")
        time.sleep(1)

        # Ждем, пока элемент для показа рабочих заданий станет доступным
        show_work_tasks = WebDriverWait(self.driver, 45).until(
            EC.presence_of_element_located((By.XPATH,
                                            "/html/body/form/div/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td[3]/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td[11]/img"))
        )

        # Кликаем для показа рабочих заданий
        show_work_tasks.click()
        time.sleep(10)
        logging.info("Выведен список рабочих заданий")

    def get_quantity_records(self):
        """Получает общее количество записей."""
        quantity_records = WebDriverWait(self.driver, 45).until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'из')]"))
        ).text
        return int(quantity_records.split('из')[1].strip())

    def click_next_page(self):
        """Нажимает кнопку "Следующая страница"."""
        WebDriverWait(self.driver, 45).until(
            EC.presence_of_element_located((By.XPATH,
                                            "/html/body/form/div/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td[3]/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td[19]/a"))
        ).click()
        time.sleep(10)

    def get_data_from_html(self, html):
        """Извлекает релевантные данные из HTML-кода страницы."""
        data_dict = {code: [] for code in self.classification_codes}  # Инициализируем словарь для данных
        soup = BeautifulSoup(html, 'lxml')

        for tr in soup.find('table', attrs={'id': 'm6a7dfd2f_tbod-tbd'}).find_all('tr'):
            row = [td.text.strip() for td in tr.find_all('td')]
            if len(row) == 26:
                new_row = row[2:-1]
                if new_row[0] and new_row[10] == 'Назначено':
                    for code in self.classification_codes:
                        if new_row[6] == code:
                            data_dict[code].append(new_row)  # Добавляем данные в соответствующий список
                            break  # Выходим из цикла, если нашли соответствие

        return data_dict  # Возвращаем словарь с данными
