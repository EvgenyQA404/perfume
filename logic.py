from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import allure


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    @allure.step('Переход на страницу')
    def get_site(self, site):
        self.driver.get(site)

    @allure.step('Нажатие на кликабельный элемент')
    def click(self, element):
        self.driver.find_element(*element).click()

    @allure.step('Ожидание до видимого элемента')
    def wait_element_located(self, element):
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(element))

    @allure.step('Ожидание до кликабельного элемента')
    def wait_element_clickable(self, element_clickable):
        WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable(element_clickable))

    @allure.step('Получение текста элемента')
    def get_text_of_element(self, text):
        return self.driver.find_element(*text).text

    @allure.step('Ввод сообщения в строку input')
    def input_text(self, string, message):
        self.driver.find_element(*string).send_keys(message)

    @allure.step('Ожидание до видимости элемента')
    def wait_text_in_element(self, locator, text):
        WebDriverWait(self.driver, 30).until(
            expected_conditions.text_to_be_present_in_element(locator, text))

    @allure.step('Ожидание изменения элемента в тексте')
    def wait_another_text(self, locator, text):
        # ожидание изменения текста
        WebDriverWait(self.driver, 30).until(lambda driver: self.driver.find_element(
            *locator).text != text)
        # возврат нового текста
        new_text = self.driver.find_element(*locator).text
        return new_text