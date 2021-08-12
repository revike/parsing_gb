from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get('https://gb.ru/login')

login = driver.find_element_by_id('user_email')
login.send_keys('revike@ya.ru')

password = driver.find_element_by_id('user_password')
password.send_keys('jhjQzly9s')

password.send_keys(Keys.ENTER)  # Нажимаем Enter

menu = driver.find_element_by_xpath(
    '//span[contains(@class, "ProductButton_button")]/..'
)
menu.click()

dropdown = driver.find_element_by_xpath(
    '//button[@data-test-id="user_dropdown_menu"]'
)
dropdown.click()

profile = driver.find_element_by_xpath(
    '//span[text()="Профиль"]/..'
).get_attribute('href')
profile.click()
