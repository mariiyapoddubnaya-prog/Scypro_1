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

    @allure.step(
        "Установить задержку вычисления {value} секунд в поле #delay"
    )
    def set_calculation_delay(self, value: int) -> None:
        """
        Вводит значение задержки в поле ввода калькулятора.
        Это параметр тестируемого приложения: калькулятор будет
        ждать указанное количество секунд перед выдачей результата.
        :param value: Время задержки в секундах (вводится в поле #delay).
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

    @allure.step("Ожидать появления спиннера загрузки")
    def wait_for_spinner(self) -> None:
        """
        Явно ожидает появления спиннера загрузки после нажатия '='.
        Демонстрирует использование явных ожиданий вместо sleep().
        """
        spinner_locator = (By.ID, "spinner")
        self.wait.until(EC.visibility_of_element_located(spinner_locator))

    @allure.step("Ожидать исчезновения спиннера и получить результат")
    def get_result(self) -> str:
        """
        Ожидает исчезновения спиннера и появления результата.
        :return: Строка с результатом вычисления.
        """
        spinner_locator = (By.ID, "spinner")
        self.wait.until(EC.invisibility_of_element_located(spinner_locator))

        result_locator = (By.CLASS_NAME, "screen")
        self.wait.until(
            EC.text_to_be_present_in_element(result_locator, "15")
        )
        return self.driver.find_element(*result_locator).text


@allure.title("Позитивный тест: вычисление суммы с задержкой")
@allure.description(
    "Проверка корректного отображения результата 15 после "
    "установки задержки 45 сек и ввода выражения 7+8=.\n"
    "Важно: set_calculation_delay(45) — это НЕ sleep(), "
    "а ввод параметра в поле тестируемого приложения."
)
@allure.severity(allure.severity_level.CRITICAL)
def test_slow_calculator_pom() -> None:
    """Тест проверяет работу калькулятора с заданной задержкой."""
    driver = webdriver.Chrome()
    try:
        with allure.step("Инициализация и открытие страницы"):
            calc_page = CalculatorPage(driver)
            calc_page.open()

        with allure.step(
            "Ввод параметра задержки 45 сек в поле #delay "
            "(это данные для тестируемого приложения, не sleep)"
        ):
            calc_page.set_calculation_delay(45)

        with allure.step("Нажатие кнопок 7, +, 8, ="):
            calc_page.click_button("7")
            calc_page.click_button("+")
            calc_page.click_button("8")
            calc_page.click_button("=")

        with allure.step("Явное ожидание спиннера загрузки"):
            calc_page.wait_for_spinner()

        with allure.step("Ожидание результата и проверка"):
            result = calc_page.get_result()
            assert result == "15", f"Ожидался '15', но получен '{result}'"
    finally:
        driver.quit()
