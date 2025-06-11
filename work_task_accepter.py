from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging
import time

class WorkTaskAccepter:
    """Класс для принятия рабочих заданий."""

    def __init__(self, driver):
        """Инициализирует экземпляр класса WorkTaskAccepter."""
        self.driver = driver

    def accept_work_tasks(self, work_tasks):
        """Принимает рабочие задания в работу."""
        for work_task in work_tasks:
            try:
                work_task_item = WebDriverWait(self.driver, 45).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/form/div/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[1]/td/div/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr/td/div/input"))
                )
                time.sleep(3)
                work_task_item.send_keys(work_task, Keys.ENTER)
                time.sleep(3)
                accept_work = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/form/div/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td[3]/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/table/tbody/tr/td/table/tbody/tr[3]/td/div/table/tbody/tr/td/table/tbody/tr/td[6]/div/table/tbody/tr/td/div/table/tbody/tr/td/button"))
                )
                if accept_work.text == "Приступить к выполнению":
                    accept_work.click()
                    time.sleep(3)
                    close_btn = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "/html/body/form/div/table[3]/tbody/tr/td[3]/table/tbody/tr[2]/td/table/tbody/tr/td/table[3]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr/td/button"))
                    )
                    close_btn.click()
                    logging.info(f"Принято в работу РЗ - {work_task}")
                    time.sleep(3)
            except Exception as e:
                logging.info(f"Не удалось принять в работу РЗ - {work_task}. Ошибка: {e}")

