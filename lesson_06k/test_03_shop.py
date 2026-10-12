from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_sauce_demo_purchase():
    # По заданию требуется Firefox. Если он снова зависнет на старте,
    # замените webdriver.Firefox() на webdriver.Chrome()
    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://www.saucedemo.com/")

        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        # Ждем загрузки следующей страницы после логина
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list")))

        # Добавляем товары в корзину
        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        driver.find_element(By.ID, "add-to-cart-sauce-labs-bolt-t-shirt").click()
        driver.find_element(By.ID, "add-to-cart-sauce-labs-onesie").click()

        # Переходим в корзину
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

        wait.until(EC.visibility_of_element_located((By.ID, "checkout")))
        driver.find_element(By.ID, "checkout").click()

        # Заполняем форму
        driver.find_element(By.ID, "first-name").send_keys("Иван")
        driver.find_element(By.ID, "last-name").send_keys("Петров")
        driver.find_element(By.ID, "postal-code").send_keys("101000")

        driver.find_element(By.ID, "continue").click()

        # Читаем итоговую стоимость
        total_element = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "summary_total_label"))
        )
        total_text = total_element.text

        # Если скриншот всё же нужен, делаем его ДО закрытия браузера!
        # (В ТЗ контрольной работы это не требуется, можно эту строку удалить)
        driver.save_screenshot("screen_03_shop.png")

        # Проверяем сумму
        assert "$58.29" in total_text, f"Ожидалась сумма $58.29, но получено: {total_text}"

    finally:
        # Гарантируем закрытие браузера в любом случае (даже если тест упадет)
        driver.quit()