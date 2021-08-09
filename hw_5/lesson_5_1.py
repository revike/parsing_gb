from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


chrome_options = Options()
# chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(
    executable_path='./chromedriver.exe', options=chrome_options)
driver.get('https://lenta.com/catalog/myaso-ptica-kolbasa/')

button_popup = driver.find_element_by_class_name(
    'delivery-address-popup__button'
)
button_popup.click()

button_cookie = driver.find_element_by_class_name(
    'cookie-usage-notice__button-inner--desktop'
)
button_cookie.click()

while True:
    try:
        button_wait = WebDriverWait(driver, 10)
        button_click = button_wait.until(
            ec.element_to_be_clickable(
                (By.CLASS_NAME, 'catalog-grid-container__pagination-button')
            ))

        button_click.click()
    except Exception as e:
        break

goods = driver.find_elements_by_class_name(
    'sku-card-small-container'
)

for good in goods:
    print(good.find_element_by_class_name(
        'sku-card-small__title'
    ).text)
