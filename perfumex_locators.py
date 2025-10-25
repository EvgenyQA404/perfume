# perfumex_locators.py — локаторы для perfumex.ru

from selenium.webdriver.common.by import By

# Главная → кнопка "Личный кабинет"
BTN_ACCOUNT = (By.XPATH, '//*[@id="header"]/div[1]/div/div/div[3]/div[2]/div/a/span/span')

# Попап логина
INPUT_EMAIL = (By.XPATH, '//*[@id="USER_LOGIN_POPUP"]')
INPUT_PASSWORD = (By.XPATH, '//*[@id="USER_PASSWORD_POPUP"]')
BTN_LOGIN = (By.XPATH, '//*[@id="avtorization-form"]/div[3]/div[2]/input')

# Признак авторизации: "кнопка Войти" исчезла (инвиз)
# Будем ждать invisibility_of_element_located(BTN_LOGIN)

# Карточка товара
PRODUCT_TITLE = (By.ID, 'pagetitle')

# Цена: на странице пример:
# <span class="values_wrapper">
#   <span class="price_value">232</span><span class="price_currency"> USD</span>
# </span>
PRICE_VALUE = (By.CSS_SELECTOR, '.values_wrapper .price_value')
PRICE_CURRENCY = (By.CSS_SELECTOR, '.values_wrapper .price_currency')
