from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time

BOT_TOKEN = "8622451849:AAFl4jjC2mr5rf2671SA3F4g3vIFcqEYwGs"
CHAT_ID = "5044500645"

SEARCH_URL = "https://www.bing.com/search?q=MOBILE+UNDER+5000&form=ANNTH1&refig=69ff69c7742d49b3ae8962ae79a76746&pc=W251"

MAX_PRICE = 5000

def send_telegram(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

sent_products = set()

while True:

    print("\nChecking deals...\n")

    driver.get(SEARCH_URL)

    time.sleep(5)

    products = driver.find_elements(
        By.XPATH,
        '//div[@data-component-type="s-search-result"]'
    )

    for item in products:

        try:

            title = item.find_element(
                By.XPATH,
                './/h2'
            ).text

            price = item.find_element(
                By.XPATH,
                './/span[contains(@class,"a-price-whole")]'
            ).text

            link = item.find_element(
                By.XPATH,
                './/a'
            ).get_attribute("href")

            price = int(price.replace(",", ""))

            print(title)
            print(price)

            if price <= MAX_PRICE:

                if link not in sent_products:

                    message = (
                        f"🔥 MOBILE DEAL FOUND 🔥\n\n"
                        f"{title}\n\n"
                        f"Price: ₹{price}\n\n"
                        f"{link}"
                    )

                    send_telegram(message)

                    print("ALERT SENT")

                    sent_products.add(link)

        except:
            pass

    print("\nWaiting 60 seconds...\n")

    time.sleep(60)