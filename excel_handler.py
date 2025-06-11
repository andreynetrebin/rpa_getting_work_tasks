from openpyxl import load_workbook
import logging

class ExcelHandler:
    """Класс для обработки операций с Excel-файлами."""

    @staticmethod
    def insert_to_xlsx(filename, data):
        """Вставляет данные в Excel-файл."""
        try:
            wb = load_workbook(filename)
            ws = wb.active
            for row in data:
                ws.append(row)
            wb.save(filename)
        except Exception as e:
            logging.critical(f'Не удалось записать данные в XLSX файл: {e}')
