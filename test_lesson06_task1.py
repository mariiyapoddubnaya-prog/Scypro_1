from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


def test_dynamic_loading():
    # Используем Chrome, так как он у вас уже успешно работает
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        # 1. Откройте страницу
        driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")

        # 2. Найдите и нажмите на кнопку "Start"
        start_button = driver.find_element(By.CSS_SELECTOR, "#start button")
        start_button.click()

        # 3. Дождитесь появления текста "Hello World!" (явное ожидание)
        finish_element = wait.until(
            EC.visibility_of_element_located((By.ID, "finish"))
        )

        # 4. Сделайте скриншот страницы (сохранится в папку с проектом)
        screenshot_path = os.path.abspath("screenshot_task1.png")
        driver.save_screenshot(screenshot_path)
        print(f"\n Скриншот сохранен: {screenshot_path}")

        # 5. Проверьте, что появившийся текст равен "Hello World!"
        assert finish_element.text == "Hello World!", \
            f"Ожидался текст 'Hello World!', но получен: '{finish_element.text}'"
        print(" Текст 'Hello World!' успешно проверен!")

    finally:
        driver.quit()


# ЭТА СТРОКА ЗАСТАВЛЯЕТ КОД РАБОТАТЬ ПРИ ОБЫЧНОМ ЗАПУСКЕ В PYCHARM
if __name__ == "__main__":
    test_dynamic_loading()