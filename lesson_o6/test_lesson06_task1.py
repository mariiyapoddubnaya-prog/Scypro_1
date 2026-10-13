import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_dynamic_loading():
    # Инициализация драйвера Chrome
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        # 1. Открытие страницы
        driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")

        # 2. Поиск и клик по кнопке Start (оптимальный CSS-селектор)
        start_button = driver.find_element(By.CSS_SELECTOR, "#start button")
        start_button.click()

        # 3. Явное ожидание появления текста Hello World!
        finish_element = wait.until(
            EC.visibility_of_element_located((By.ID, "finish"))
        )

        # 4. Создание скриншота в текущей директории
        screenshot_name = "screenshot_task1.png"
        driver.save_screenshot(screenshot_name)

        # 5. Проверка (assert) появившегося текста
        assert finish_element.text == "Hello World!", \
            f"Ожидался текст 'Hello World!', но получен: '{finish_element.text}'"

    finally:
        # Гарантированное закрытие браузера
        driver.quit()