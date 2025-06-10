from pages.cadastro_page import CadastroPage
from utils.base_test import iniciar_driver

def test_cadastros():
    driver = iniciar_driver()
    cadastro_page = CadastroPage(driver)

    cenarios = [
        {"username": "Vitoria576", "password": "4561"},
        {"username": "", "password": "123"},
        {"username": "teste12", "password": ""}
    ]

    for c in cenarios:
        resultado = cadastro_page.cadastrar_usuario(c["username"], c["password"])
        print(f"Cadastro ({c['username']}): {resultado}")

    driver.quit()
