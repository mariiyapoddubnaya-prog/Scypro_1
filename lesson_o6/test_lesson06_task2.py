from selenium import webdriver


def test_session_storage_auth():
    driver = webdriver.Chrome()

    try:
        # 1. Откройте страницу
        driver.get("https://gitflic.ru/")

        # 2. Установите cookie пользователя 1 (ЗАМЕНИТЕ ДАННЫЕ НА РЕАЛЬНЫЕ!)
        cookie_user1 = {
            "name": "_gitflic_session",  # Проверьте реальное имя в браузере
            "value": "ВСТАВЬТЕ_СЮДА_РЕАЛЬНОЕ_ЗНАЧЕНИЕ_COOKIE_1",
            "domain": ".gitflic.ru"
        }
        driver.add_cookie(cookie_user1)

        # 3. Обновите страницу
        driver.refresh()

        # 4. Перейдите на страницу пользователя 1 (замените user1_login на реальный)
        driver.get("https://gitflic.ru/user/user1_login")
        url_user1 = driver.current_url
        print(f"\n URL пользователя 1: {url_user1}")

        # 5. Разлогиньтесь (очистите куки)
        driver.delete_all_cookies()

        # 6. Установите cookie пользователя 2 (ЗАМЕНИТЕ ДАННЫЕ НА РЕАЛЬНЫЕ!)
        cookie_user2 = {
            "name": "_gitflic_session",  # Проверьте реальное имя в браузере
            "value": "ВСТАВЬТЕ_СЮДА_РЕАЛЬНОЕ_ЗНАЧЕНИЕ_COOKIE_2",
            "domain": ".gitflic.ru"
        }
        driver.add_cookie(cookie_user2)

        # 7. Обновите страницу
        driver.refresh()

        # 8. Перейдите на страницу пользователя 2 (замените user2_login на реальный)
        driver.get("https://gitflic.ru/user/user2_login")
        url_user2 = driver.current_url
        print(f" URL пользователя 2: {url_user2}")

        # 9. Проверьте, что URL различаются
        assert url_user1 != url_user2, "URL профилей пользователей не должны совпадать"
        print(" URLs успешно различаются!")

    finally:
        driver.quit()


# ЭТА СТРОКА ЗАСТАВЛЯЕТ КОД РАБОТАТЬ ПРИ ОБЫЧНОМ ЗАПУСКЕ В PYCHARM
if __name__ == "__main__":
    test_session_storage_auth()
