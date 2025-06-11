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

    def __init__(self, driver):
        """Инициализирует экземпляр класса DataExtractor."""
        self.driver = driver

    def extract_data(self):
        """Извлекает релевантные данные из веб-приложения."""
        self.login_and_navigate()  # Выполняем вход и переходим к нужной странице
        quantity_records = self.get_quantity_records()  # Получаем общее количество записей

        list_53_12_1, list_53_13 = [], []
        for _ in range(math.ceil(quantity_records / 20)):  # Итерируемся по страницам данных
            html = self.driver.page_source
            data_53_12_1, data_53_13 = self.get_data_from_html(html)
            list_53_12_1.extend(data_53_12_1)
            list_53_13.extend(data_53_13)

            if _ < math.ceil(quantity_records / 20) - 1:
                self.click_next_page()  # Переходим на следующую страницу

        logging.info(f"Всего получено строк: {len(list_53_12_1) + len(list_53_13)}")
        work_tasks = [work_task[0] for work_task in list_53_13 + list_53_12_1]

        # Используем WorkTaskAccepter для принятия рабочих заданий
        task_accepter = WorkTaskAccepter(self.driver)
        task_accepter.accept_work_tasks(work_tasks)

        return list_53_12_1, list_53_13

    # Остальной код DataExtractor остается без изменений
    def login_and_navigate(self):
        """Выполняет вход в приложение и переходит к разделу 'Рабочие задания'."""
        self.navigate_to_work_tasks()
        self.hover_over_work_tasks()

    def navigate_to_work_tasks(self):
        """Переходит к разделу 'Рабочие задания'."""
        action = ActionChains(self.driver)
        element = WebDriverWait(self.driver, 45).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/form/div/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td[1]/div/table/tbody/tr/td/div/div[2]/div[1]/div[2]/div/ul/li[7]"))
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
        number_cls = WebDriverWait(self.driver, 45).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/form/div/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td[3]/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[2]/td[9]/input"))
        )
        number_cls = self.driver.find_element(By.XPATH, "/html/body/form/div/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td[3]/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[2]/td[9]/input")
        time.sleep(1)
        status = WebDriverWait(self.driver, 45).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/form/div/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td[3]/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[2]/td[13]/input"))
        )
        number_cls.send_keys("=53.12.1.,=53.13.")
        time.sleep(1)
        status.send_keys("=Назначено")
        time.sleep(1)

        show_work_tasks = WebDriverWait(self.driver, 45).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/form/div/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td[3]/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td[11]/img"))
        )

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
            EC.presence_of_element_located((By.XPATH, "/html/body/form/div/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td[3]/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td[19]/a"))
        ).click()
        time.sleep(10)

    def get_data_from_html(self, html):
        """Извлекает релевантные данные из HTML-кода страницы."""
        data_53_13 = []
        data_53_12_1 = []
        soup = BeautifulSoup(html, 'lxml')
        for tr in soup.find('table', attrs={'id': 'm6a7dfd2f_tbod-tbd'}).find_all('tr'):
            row = [td.text.strip() for td in tr.find_all('td')]
            if len(row) == 26:
                new_row = row[2:-1]
                if new_row[0] and new_row[10] == 'Назначено':
                    if new_row[6] == '53.13.':
                        data_53_13.append(new_row)
                    elif new_row[6] == '53.12.1.':
                        data_53_12_1.append(new_row)
        return data_53_12_1, data_53_13

