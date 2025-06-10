from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CadastroPage:
    def __init__(self, driver):
        self.driver = driver
        self.btn_cadastro = (By.ID, "signin2")
        self.modal = (By.ID, "signInModal")
        self.username = (By.ID, "sign-username")
        self.password = (By.ID, "sign-password")
        self.btn_confirmar = (By.XPATH, "//button[contains(text(),'Sign up')]")

    def abrir_modal(self):
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.btn_cadastro)).click()
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.modal))

    def cadastrar_usuario(self, username, password):
        self.abrir_modal()
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.username)).send_keys(username)
        self.driver.find_element(*self.password).send_keys(password)
        self.driver.find_element(*self.btn_confirmar).click()
        try:
            alert = WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            texto = alert.text
            alert.accept()
            return texto
        except:
            return "nenhum alerta apareceu"
