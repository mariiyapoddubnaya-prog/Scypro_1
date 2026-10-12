from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_form_submission():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://bonigarcia.dev/selenium-webdriver-java/data-types.html")

        # Используем By.NAME, так как у полей ввода нет id, только name
        driver.find_element(By.NAME, "first-name").send_keys("Иван")
        driver.find_element(By.NAME, "last-name").send_keys("Петров")
        driver.find_element(By.NAME, "address").send_keys("Ленина, 55-3")
        driver.find_element(By.NAME, "e-mail").send_keys("test@skypro.com")
        driver.find_element(By.NAME, "phone").send_keys("+7985899998787")
        # Zip code оставляем пустым
        driver.find_element(By.NAME, "city").send_keys("Москва")
        driver.find_element(By.NAME, "country").send_keys("Россия")
        driver.find_element(By.NAME, "job-position").send_keys("QA")
        driver.find_element(By.NAME, "company").send_keys("SkyPro")

        # скриншот
        driver.save_screenshot("screen_01.png")

        # Находим кнопку Submit
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        # Прокручиваем страницу до кнопки, чтобы она оказалась в видимой области
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)

        # Кликаем с помощью JavaScript (это обходит проблему перекрытия элемента footer-ом)
        driver.execute_script("arguments[0].click();", submit_button)

        # Ждем загрузки новой страницы и появления блока с результатами
        zip_code_result = wait.until(
            EC.presence_of_element_located((By.ID, "zip-code"))
        )

        # Проверяем, что Zip code подсвечен красным (класс alert-danger)
        assert "alert-danger" in zip_code_result.get_attribute("class"), \
            "Поле Zip code должно иметь класс alert-danger"

        # Проверяем, что остальные поля подсвечены зеленым (класс alert-success)
        fields_to_check = ["first-name", "last-name", "e-mail", "city"]
        for field_id in fields_to_check:
            field = driver.find_element(By.ID, field_id)
            assert "alert-success" in field.get_attribute("class"), \
                f"Поле {field_id} должно иметь класс alert-success"

    finally:
        driver.quit()