from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.btn_login = (By.ID, "login2")
        self.input_username = (By.ID, "loginusername")
        self.input_password = (By.ID, "loginpassword")
        self.btn_submit_login = (By.XPATH, "//button[contains(@class,'btn btn-primary') and contains(text(),'Log in')]")
        self.btn_logout = (By.ID, "logout2")

    def abrir_login_modal(self):
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(self.btn_login)).click()

    def preencher_credenciais(self, username, password):
        WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(self.input_username)).send_keys(username)
        self.driver.find_element(*self.input_password).send_keys(password)

    def submeter_login(self):
        self.driver.find_element(*self.btn_submit_login).click()

    def login(self, username, password):
        self.abrir_login_modal()
        self.preencher_credenciais(username, password)
        self.submeter_login()
        try:
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.btn_logout))
            return "login_sucesso"
        except:
            return "login_falhou"

    def logout(self):
        try:
            btn = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(self.btn_logout))
            btn.click()
            return "logout_sucesso"
        except:
            return "logout_falhou"
