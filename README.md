# RPA Скрипт для Автоматизированного Приема Заявок в IBM SmartCloud Control Desk

## Описание

Этот скрипт автоматизирует процесс извлечения данных о рабочих заданиях (заявках) из веб-интерфейса системы IBM SmartCloud Control Desk, их принятия в работу и сохранения в Excel-файлы для дальнейшей обработки или отчетности.

## Предварительные требования

*   Python 3.6+
*   Установленные библиотеки (см. раздел "Установка")
*   Chrome Browser
*   Chrome Driver (поместите в папку `driver/`)
*   Доступ к системе IBM SmartCloud Control Desk с необходимыми правами.

## Установка

1.  Клонируйте репозиторий:

    ```bash
    git clone <your_repository_url>
    ```

2.  Перейдите в директорию проекта:

    ```bash
    cd <your_project_directory>
    ```

3.  Создайте виртуальное окружение (рекомендуется):

    ```bash
    python -m venv venv
    ```

4.  Активируйте виртуальное окружение:

    *   Windows:

        ```bash
        venv\Scripts\activate
        ```

    *   macOS и Linux:

        ```bash
        source venv/bin/activate
        ```

5.  Установите необходимые библиотеки:

    ```bash
    pip install -r requirements.txt
    ```

## Настройка

1.  Создайте файл `config.ini` в корневой директории проекта.
2.  Заполните файл `config.ini` вашими учетными данными и URL веб-приложения IBM SmartCloud Control Desk:

    ```ini
    [web_address]
    url = your_smartcloud_url

    [user]
    login = your_username
    password = your_password

    [classifications]
    codes = classification_code_1, classification_code_2, classification_code_N.
    ```

    Замените `your_smartcloud_url`, `your_username`, `your_password` и classification_code на ваши фактические данные для доступа к IBM SmartCloud Control Desk.
3.  Убедитесь, что Chrome Driver находится в папке `driver/`.  Скачать Chrome Driver можно по ссылке: [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads).  Версия Chrome Driver должна соответствовать версии вашего Chrome браузера.

## Использование

1.  Запустите скрипт `main.py`:

    ```bash
    python main.py
    ```

2.  Скрипт выполнит следующие действия:

    *   Авторизуется в веб-интерфейсе IBM SmartCloud Control Desk.
    *   Перейдет в раздел "Рабочие задания" (заявки).
    *   Извлечет данные о рабочих заданиях (заявках) с кодами, указанными в конфигурационном файле, со статусом "Назначено".  **Примечание:** Эти коды могут быть настроены в скрипте `data_extractor.py` в соответствии с вашей конфигурацией IBM SmartCloud Control Desk.
    *   Примет каждое рабочее задание в работу.
    *   Сохранит извлеченные данные в Excel файлы.
    *   Запишет логи работы скрипта в папку `logs/`.

## Важные замечания

*   **Конфигурация IBM SmartCloud Control Desk:**  Убедитесь, что статус ("Назначено") соответствует вашей конфигурации IBM SmartCloud Control Desk.  При необходимости измените статус в скрипте `data_extractor.py`.
*   **Права доступа:**  Учетная запись, используемая для запуска скрипта, должна иметь достаточные права для просмотра и принятия рабочих заданий в IBM SmartCloud Control Desk.
*   **XPATH-выражения:**  Скрипт использует XPATH-выражения для поиска элементов на веб-странице.  Эти выражения могут быть несовместимы с другими версиями или конфигурациями IBM SmartCloud Control Desk.  При необходимости измените их в соответствующих файлах (`data_extractor.py`, `work_task_accepter.py`).
*   **Headless режим:** Скрипт по умолчанию запускается в headless режиме (без отображения окна браузера).  Для отладки можно временно отключить headless режим в файле `web_driver.py`.

## Структура проекта

```
.
├── config.ini # Файл конфигурации с учетными данными
├── config.py # Модуль для загрузки конфигурации
├── data_extractor.py # Модуль для извлечения данных из веб-приложения
├── driver/ # Директория с Chrome Driver
│ └── chromedriver.exe
├── excel_handler.py # Модуль для работы с Excel-файлами
├── logger.py # Модуль для настройки логирования
├── logs/ # Директория для хранения логов
├── main.py # Основной скрипт для запуска RPA
├── README.md # Этот файл
├── requirements.txt # Файл со списком зависимостей
├── web_driver.py # Модуль для управления WebDriver
└── work_task_accepter.py # Модуль для принятия рабочих заданий
```


## Зависимости

*   selenium
*   beautifulsoup4
*   openpyxl
*   configparser

Все зависимости перечислены в файле `requirements.txt`.

## Логирование

Скрипт ведет логи своей работы в папку `logs/`.  В логах записываются все важные события, ошибки и предупреждения.
