# Автотесты UI с использованием Page Object и Allure

Этот проект содержит UI-автотесты для калькулятора и интернет-магазина, написанные на Python с использованием библиотек `selenium`, `pytest` и `allure-pytest`.

##  Требования

- Python 3.8+
- Установленные зависимости: `selenium`, `pytest`, `allure-pytest`
- Установленный [Allure Commandline](https://allurereport.org/docs/install/) (для генерации отчета)

##  Как запустить тесты и сформировать отчет

1. Убедитесь, что вы находитесь в корневой папке проекта.
2. Запустите тесты с указанием директории для сохранения результатов Allure:
   ```bash
   pytest lesson_10/ --alluredir=./allure-results -v