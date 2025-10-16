from selenium.webdriver.common.by import By

price = (By.XPATH, "//span[contains(@class, 'price__new-val') and contains(text(), '₽')]")
product = (By.XPATH, "//h1[contains(@class, 'switcher-title')]")