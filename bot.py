import requests
from bs4 import BeautifulSoup
import time

BOT_TOKEN = "8622451849:AAFl4jjC2mr5rf2671SA3F4g3vIFcqEYwGs"
CHAT_ID = "5044500645"

products = [
    {
        "name": "Amazon Mobile Deals",
        "url": "https://www.amazon.in/s?k=smartphone+under+5000",
        "target_price": 50000
    }
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

def send_telegram_message(message):

    send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(send_url, data=data)

while True:

    print("Checking Deals...")

    for product in products:

        try:

            page = requests.get(product["url"], headers=headers)

            soup = BeautifulSoup(page.content, "html.parser")

            price_tag = soup.find("span", class_="a-price-whole")

            if price_tag:

                current_price = int(
                    price_tag.text.replace(",", "").replace(".", "")
                )

                print("CURRENT PRICE:", current_price)

                if current_price <= product["target_price"]:

                    message = (
                        f"🔥 DEAL ALERT 🔥\n\n"
                        f"Price: ₹{current_price}\n\n"
                        f"{product['url']}"
                    )

                    send_telegram_message(message)

                    print("TELEGRAM ALERT SENT")

                else:
                    print("Price Still High")

            else:
                print("Price Not Found")

        except Exception as e:
            print("ERROR:", e)

    print("Checking again in 60 seconds...\n")

    time.sleep(60)