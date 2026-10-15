import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.saucedemo.com/"

    def open(self):
        self.driver.get(self.url)

    def login(self, username, password):
        self.driver.find_element(By.ID, "user-name").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "login-button").click()
        # Ждем перехода на страницу товаров после логина
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("inventory.html")
        )


class MainShopPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def add_to_cart(self, item_id):
        locator = (By.ID, item_id)
        self.wait.until(EC.visibility_of_element_located(locator))
        self.driver.find_element(*locator).click()

    def go_to_cart(self):
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        # Ждем загрузки страницы корзины
        self.wait.until(EC.url_contains("cart.html"))


class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click_checkout(self):
        checkout_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "checkout"))
        )
        checkout_btn.click()


class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def fill_info(self, first_name, last_name, zip_code):
        self.driver.find_element(By.ID, "first-name").send_keys(first_name)
        self.driver.find_element(By.ID, "last-name").send_keys(last_name)
        self.driver.find_element(By.ID, "postal-code").send_keys(zip_code)

    def click_continue(self):
        self.driver.find_element(By.ID, "continue").click()

    def get_total(self):
        total_locator = (By.CLASS_NAME, "summary_total_label")
        total_element = self.wait.until(
            EC.visibility_of_element_located(total_locator)
        )
        return total_element.text


def test_shop_purchase_pom():
    chrome_options = Options()

    # 1. Отключаем менеджер паролей и уведомления
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # 2. Убираем плашку "Chrome управляется автоматизированным ПО"
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-automation"]
    )

    # 3. ГЛАВНОЕ ИСПРАВЛЕНИЕ: Отключаем проверку утечки паролей Chrome
    chrome_options.add_argument("--disable-features=PasswordLeakDetection")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-notifications")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        main_page = MainShopPage(driver)
        main_page.add_to_cart("add-to-cart-sauce-labs-backpack")
        main_page.add_to_cart("add-to-cart-sauce-labs-bolt-t-shirt")
        main_page.add_to_cart("add-to-cart-sauce-labs-onesie")
        main_page.go_to_cart()

        cart_page = CartPage(driver)
        cart_page.click_checkout()

        checkout_page = CheckoutPage(driver)
        checkout_page.fill_info("Иван", "Петров", "101000")
        checkout_page.click_continue()

        total_text = checkout_page.get_total()
        driver.quit()

        assert "$58.29" in total_text, (
            f"Ожидалась $58.29, но получено: {total_text}"
        )
    except Exception:
        # Сохраняем скриншот с абсолютным путем, чтобы вы его точно нашли
        error_path = os.path.abspath("shop_test_error.png")
        driver.save_screenshot(error_path)
        print(f"\n ОШИБКА! Скриншот сохранен здесь: {error_path}")
        driver.quit()
        raise
