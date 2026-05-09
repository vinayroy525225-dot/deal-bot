import requests
from bs4 import BeautifulSoup
import time

BOT_TOKEN = "8622451849:AAFl4jjC2mr5rf2671SA3F4g3vIFcqEYwGs"
CHAT_ID = "5044500645"

products = [

    {
        "name": "OPPO K13 5G",
        "url": "https://www.amazon.in/s?k=oppo+k13+5g",
        "target_price": 8000
    },

    {
        "name": "Samsung Galaxy",
        "url": "https://www.amazon.in/s?k=samsung+5g+mobile",
        "target_price": 7000
    },

    {
        "name": "Redmi Note",
        "url": "https://www.flipkart.com/search?q=redmi+note",
        "target_price": 7500
    }

]

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120 Safari/537.36"
    )
}

sent_deals = set()

def send_telegram(message):

    telegram_url = (
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    )

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(telegram_url, data=data)

while True:

    print("Checking Premium Phone Deals...\n")

    for product in products:

        try:

            response = requests.get(
                product["url"],
                headers=headers,
                timeout=15
            )

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            prices = soup.find_all(
                "span",
                class_="a-price-whole"
            )

            for p in prices:

                try:

                    current_price = int(
                        p.text.replace(",", "")
                              .replace(".", "")
                    )

                    print(
                        product["name"],
                        "₹",
                        current_price
                    )

                    if current_price <= product["target_price"]:

                        deal_key = (
                            f"{product['name']}_{current_price}"
                        )

                        if deal_key not in sent_deals:

                            msg = (
                                f"🔥 CRAZY DEAL FOUND 🔥\n\n"
                                f"{product['name']}\n\n"
                                f"Current Price: ₹{current_price}\n"
                                f"Target Price: ₹{product['target_price']}\n\n"
                                f"BUY FAST:\n"
                                f"{product['url']}"
                            )

                            send_telegram(msg)

                            sent_deals.add(deal_key)

                            print("ALERT SENT\n")

                except:
                    pass

        except Exception as e:
            print("ERROR:", e)

    print("Checking again in 60 sec...\n")

    time.sleep(60)