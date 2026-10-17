import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature("Калькулятор")
class CalculatorPage:
    """Класс для взаимодействия со страницей медленного калькулятора."""

    def __init__(self, driver: webdriver.Chrome) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 50)
        self.url = (
            "https://bonigarcia.dev/selenium-webdriver-java/"
            "slow-calculator.html"
        )

    @allure.step("Открыть страницу калькулятора")
    def open(self) -> None:
        """Переходит на URL страницы калькулятора."""
        self.driver.get(self.url)

    @allure.step("Установить задержку {value} секунд")
    def set_delay(self, value: int) -> None:
        """
        Вводит значение задержки в поле ввода.
        :param value: Время задержки в секундах.
        """
        delay_input = self.driver.find_element(By.ID, "delay")
        delay_input.clear()
        delay_input.send_keys(str(value))

    @allure.step("Нажать кнопку '{button_text}'")
    def click_button(self, button_text: str) -> None:
        """
        Находит и кликает по кнопке калькулятора по её тексту.
        :param button_text: Текст на кнопке (например, '7', '+', '=').
        """
        locator = (By.XPATH, f"//span[text()='{button_text}']")
        self.driver.find_element(*locator).click()

    @allure.step("Получить результат вычисления")
    def get_result(self) -> str:
        """
        Ожидает появления результата и возвращает его текст.
        :return: Строка с результатом вычисления.
        """
        result_locator = (By.CLASS_NAME, "screen")
        self.wait.until(
            EC.text_to_be_present_in_element(result_locator, "15")
        )
        return self.driver.find_element(*result_locator).text


@allure.title("Позитивный тест: вычисление суммы с задержкой")
@allure.description(
    "Проверка корректного отображения результата 15 после "
    "установки задержки 45 сек и ввода выражения 7+8="
)
@allure.severity(allure.severity_level.CRITICAL)
def test_slow_calculator_pom() -> None:
    """Тест проверяет работу калькулятора с заданной задержкой."""
    driver = webdriver.Chrome()
    try:
        with allure.step("Инициализация и открытие страницы"):
            calc_page = CalculatorPage(driver)
            calc_page.open()

        with allure.step("Ввод параметров и нажатие кнопок"):
            calc_page.set_delay(45)
            calc_page.click_button("7")
            calc_page.click_button("+")
            calc_page.click_button("8")
            calc_page.click_button("=")

        with allure.step("Проверка полученного результата"):
            result = calc_page.get_result()
            assert result == "15", f"Ожидался '15', но получен '{result}'"
    finally:
        driver.quit()
