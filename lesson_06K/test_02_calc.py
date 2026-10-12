from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_slow_calculator():
    driver = webdriver.Chrome()
    # Таймаут 50 секунд, так как задержка в калькуляторе составляет 45 секунд
    wait = WebDriverWait(driver, 50)

    try:
        driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")

        delay_input = wait.until(
            EC.visibility_of_element_located((By.ID, "delay"))
        )
        delay_input.clear()
        delay_input.send_keys("45")

        # Используем XPath по тексту для кнопок калькулятора
        driver.find_element(By.XPATH, "//span[text()='7']").click()
        driver.find_element(By.XPATH, "//span[text()='+']").click()
        driver.find_element(By.XPATH, "//span[text()='8']").click()
        driver.find_element(By.XPATH, "//span[text()='=']").click()

        # скриншот
        driver.save_screenshot("screen_02.png")

        # Ждем появления текста "15" в элементе с классом "screen" (а не id="result")
        wait.until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "screen"), "15")
        )

        final_result = driver.find_element(By.CLASS_NAME, "screen").text
        assert final_result == "15", f"Ожидался результат '15', но получен '{final_result}'"

    finally:
        driver.quit()