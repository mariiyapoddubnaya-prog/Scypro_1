from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CalculatorPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 50)
        self.url = (
            "https://bonigarcia.dev/selenium-webdriver-java/"
            "slow-calculator.html"
        )

    def open(self):
        self.driver.get(self.url)

    def set_delay(self, value):
        delay_input = self.driver.find_element(By.ID, "delay")
        delay_input.clear()
        delay_input.send_keys(str(value))

    def click_button(self, button_text):
        locator = (By.XPATH, f"//span[text()='{button_text}']")
        self.driver.find_element(*locator).click()

    def get_result(self):
        result_locator = (By.CLASS_NAME, "screen")
        self.wait.until(
            EC.text_to_be_present_in_element(result_locator, "15")
        )
        return self.driver.find_element(*result_locator).text


def test_slow_calculator_pom():
    driver = webdriver.Chrome()
    try:
        calc_page = CalculatorPage(driver)
        calc_page.open()
        calc_page.set_delay(45)
        calc_page.click_button("7")
        calc_page.click_button("+")
        calc_page.click_button("8")
        calc_page.click_button("=")

        result = calc_page.get_result()
        assert result == "15", (
            f"Ожидался '15', но получен '{result}'"
        )
    finally:
        driver.quit()
