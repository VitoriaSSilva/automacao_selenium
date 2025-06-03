from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import traceback

def iniciar_Drive():
    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--guest")  # Modo convidado (sem perfil)
    # chrome_options.add_argument("--incognito")  # Alternativa: modo anônimo

    chrome_options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    })

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://demoblaze.com/")
    return driver


def elemento_visivel(driver, by, valor, timeout=2):
    try:
        return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, valor)))
    except:
        return None

def fechar_modal(driver, modal_id):
    close_btn = elemento_visivel(driver, By.XPATH, f"//div[@id='{modal_id}']//button[text()='Close']", timeout=1)
    if close_btn:
        close_btn.click()
        time.sleep(0.5)

def inserir_Dados(driver, username, password):
    fechar_modal(driver, "logInModal")
    fechar_modal(driver, "signInModal")

    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "signin2"))).click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "signInModal")))

    username_field = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "sign-username")))
    username_field.clear()
    username_field.send_keys(username)

    password_field = driver.find_element(By.ID, "sign-password")
    password_field.clear()
    password_field.send_keys(password)

    driver.find_element(By.XPATH, "//button[contains(@class,'btn') and contains(text(),'Sign up')]").click()

    try:
        alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
        text = alert.text
        alert.accept()
        return text
    except:
        return "nenhum alerta apareceu"

def fazer_login(driver, username, password):
    fechar_modal(driver, "signInModal")

    try:
        login_btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, "login2")))
    except:
        print("Botão de login não está disponível — talvez já esteja logado.")
        return

    login_btn.click()

    # Aguarde o campo de usuário aparecer
    login_user = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, "loginusername")))
    login_pass = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, "loginpassword")))

    login_user.clear()
    login_user.send_keys(username)
    login_pass.clear()
    login_pass.send_keys(password)

    driver.find_element(By.XPATH, "//button[contains(@class,'btn btn-primary') and contains(text(),'Log in')]").click()

    # Aguarda até aparecer o botão logout para confirmar login 
    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "logout2")))
        print("[INFO] Login provavelmente foi bem-sucedido.")
    except:
        print("[INFO] Login falhou ou não foi reconhecido.")

    # Trata alertas que possam aparecer 
    try:
        alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
        print(f"[ALERTA APÓS LOGIN] {alert.text}")
        alert.accept()
    except:
        print("[INFO] Nenhum alerta apareceu após login.")


def fazer_logout(driver):
    logout_btn = elemento_visivel(driver, By.ID, "logout2", timeout=3)
    if logout_btn:
        try:
            logout_btn.click()
            time.sleep(0.5)
            print("Logout realizado com sucesso.")
        except Exception as e:
            print(f"Erro ao clicar no logout: {e}")
    else:
        print("Botão de logout não está visível. Não está logado ou já saiu.")

def main():
    try:
        driver = iniciar_Drive()
        time.sleep(1)

        inputs = [
            {"tipo": "cadastro", "username": "Vitoria576", "password": "4561"},
            {"tipo": "cadastro", "username": "", "password": "123"},
            {"tipo": "cadastro", "username": "teste12", "password": ""},
            {"tipo": "login", "username": "vitoria12", "password": "1234"},
            {"tipo": "login", "username": "kakak", "password": "1234"},
            {"tipo": "login", "username": "vitoria12", "password": "hvytck"},
            {"tipo": "login", "username": "vitoria12", "password": ""},
            {"tipo": "login", "username": "", "password": "1234"},
            {"tipo": "login", "username": "kiki", "password": "456"},
            {"tipo": "login", "username": "", "password": ""}
        ]

        for c in inputs:
            try:
                fechar_modal(driver, "logInModal")
                fechar_modal(driver, "signInModal")

                if c["tipo"] == "cadastro":
                    resultado = inserir_Dados(driver, c["username"], c["password"])
                    print(f"Cenário - Cadastro ({c['username']}): {resultado}")
                elif c["tipo"] == "login":
                    fazer_login(driver, c["username"], c["password"])
                    print(f"Cenário - Login tentado com ({c['username']})")
                    fazer_logout(driver)

                time.sleep(0.5)

            except Exception as e:
                print(f"Erro no cenário ({c['tipo']}, usuário: {c['username']}): {e}")
                traceback.print_exc()
    finally:
        driver.quit()

main()
