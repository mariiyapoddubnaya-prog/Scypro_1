import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature("Интернет-магазин")
class LoginPage:
    """Класс для взаимодействия со страницей авторизации."""

    def __init__(self, driver: webdriver.Chrome) -> None:
        self.driver = driver
        self.url = "https://www.saucedemo.com/"

    @allure.step("Открыть страницу авторизации")
    def open(self) -> None:
        """Переходит на URL страницы логина."""
        self.driver.get(self.url)

    @allure.step("Выполнить вход с логином {username}")
    def login(self, username: str, password: str) -> None:
        """
        Вводит учетные данные и нажимает кнопку входа.
        :param username: Имя пользователя.
        :param password: Пароль пользователя.
        """
        self.driver.find_element(By.ID, "user-name").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "login-button").click()


@allure.feature("Интернет-магазин")
class MainShopPage:
    """Класс для взаимодействия с главной страницей магазина."""

    def __init__(self, driver: webdriver.Chrome) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Добавить товар '{item_id}' в корзину")
    def add_to_cart(self, item_id: str) -> None:
        """
        Ожидает появления товара и добавляет его в корзину.
        :param item_id: HTML ID кнопки добавления товара.
        """
        locator = (By.ID, item_id)
        self.wait.until(EC.visibility_of_element_located(locator))
        self.driver.find_element(*locator).click()

    @allure.step("Перейти в корзину")
    def go_to_cart(self) -> None:
        """Кликает на иконку корзины."""
        self.driver.find_element(
            By.CLASS_NAME, "shopping_cart_link"
        ).click()


@allure.feature("Интернет-магазин")
class CartPage:
    """Класс для взаимодействия со страницей корзины."""

    def __init__(self, driver: webdriver.Chrome) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Нажать кнопку оформления заказа (Checkout)")
    def click_checkout(self) -> None:
        """Ожидает доступности кнопки и кликает по ней."""
        checkout_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "checkout"))
        )
        checkout_btn.click()


@allure.feature("Интернет-магазин")
class CheckoutPage:
    """Класс для взаимодействия со страницей оформления заказа."""

    def __init__(self, driver: webdriver.Chrome) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Заполнить данные покупателя")
    def fill_info(
            self, first_name: str, last_name: str, zip_code: str
    ) -> None:
        """
        Заполняет форму контактными данными.
        :param first_name: Имя.
        :param last_name: Фамилия.
        :param zip_code: Почтовый индекс.
        """
        self.driver.find_element(By.ID, "first-name").send_keys(
            first_name
        )
        self.driver.find_element(By.ID, "last-name").send_keys(
            last_name
        )
        self.driver.find_element(By.ID, "postal-code").send_keys(
            zip_code
        )

    @allure.step("Нажать кнопку Continue")
    def click_continue(self) -> None:
        """Подтверждает введенные данные и переходит к итогу."""
        self.driver.find_element(By.ID, "continue").click()

    @allure.step("Получить итоговую стоимость заказа")
    def get_total(self) -> str:
        """
        Ожидает появления блока с итоговой суммой.
        :return: Строка с итоговой стоимостью (например, 'Total: $58.29').
        """
        total_locator = (By.CLASS_NAME, "summary_total_label")
        total_element = self.wait.until(
            EC.visibility_of_element_located(total_locator)
        )
        return total_element.text


@allure.title("Позитивный тест: полное оформление заказа")
@allure.description(
    "Проверка полного цикла покупки: логин, добавление 3 товаров, "
    "переход в корзину, заполнение данных и проверка итоговой суммы."
)
@allure.severity(allure.severity_level.CRITICAL)
def test_shop_purchase_pom() -> None:
    """Тест проверяет успешное завершение покупки в магазине."""
    driver = webdriver.Chrome()
    try:
        with allure.step("Авторизация в системе"):
            login_page = LoginPage(driver)
            login_page.open()
            login_page.login("standard_user", "secret_sauce")

        with allure.step("Добавление товаров в корзину"):
            main_page = MainShopPage(driver)
            main_page.add_to_cart("add-to-cart-sauce-labs-backpack")
            main_page.add_to_cart("add-to-cart-sauce-labs-bolt-t-shirt")
            main_page.add_to_cart("add-to-cart-sauce-labs-onesie")
            main_page.go_to_cart()

        with allure.step("Переход к оформлению заказа"):
            cart_page = CartPage(driver)
            cart_page.click_checkout()

        with allure.step("Заполнение данных и завершение"):
            checkout_page = CheckoutPage(driver)
            checkout_page.fill_info("Иван", "Петров", "101000")
            checkout_page.click_continue()
            total_text = checkout_page.get_total()

        with allure.step("Проверка итоговой суммы"):
            assert "$58.29" in total_text, (
                f"Ожидалась $58.29, но получено: {total_text}"
            )
    except Exception:
        driver.quit()
        raise
    finally:
        driver.quit()
