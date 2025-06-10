from pages.login_page import LoginPage
from utils.base_test import iniciar_driver
import time

def test_logins():
    driver = iniciar_driver()
    login_page = LoginPage(driver)

    cenarios = [
        {"username": "vitoria12", "password": "1234"},
        {"username": "kakak", "password": "1234"},
        {"username": "vitoria12", "password": "hvytck"},
        {"username": "vitoria12", "password": ""},
        {"username": "", "password": "1234"},
        {"username": "kiki", "password": "456"},
        {"username": "", "password": ""}
    ]

    for c in cenarios:
        resultado = login_page.login(c["username"], c["password"])
        print(f"Login ({c['username']}): {resultado}")
        if resultado == "login_sucesso":
            time.sleep(1)
            login_page.logout()

    driver.quit()
