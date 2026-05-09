import requests
from bs4 import BeautifulSoup
import time

BOT_TOKEN = "8622451849:AAFl4jjC2mr5rf2671SA3F4g3vIFcqEYwGs"
CHAT_ID = "5044500645"

products = [
    {
        "name": "Phone Deals",
        "url": "https://www.amazon.in/s?k=smartphone+under+5000",
        "target_price": 50000
    }
]

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9"
}

def send_telegram(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)

while True:

    print("Checking Deals...\n")

    for product in products:

        try:

            response = requests.get(
                product["url"],
                headers=headers
            )

            soup = BeautifulSoup(response.text, "html.parser")

            prices = soup.find_all("span", class_="a-price-whole")

            found = False

            for p in prices:

                try:

                    current_price = int(
                        p.text.replace(",", "").replace(".", "")
                    )

                    print("PRICE FOUND:", current_price)

                    if current_price <= product["target_price"]:

                        found = True

                        msg = (
                            f"🔥 DEAL ALERT 🔥\n\n"
                            f"Price: ₹{current_price}\n"
                            f"Target: ₹{product['target_price']}\n\n"
                            f"{product['url']}"
                        )

                        send_telegram(msg)

                        print("TELEGRAM ALERT SENT\n")

                        break

                except:
                    pass

            if not found:
                print("No Deal Found\n")

        except Exception as e:
            print("ERROR:", e)

    print("Checking again in 60 sec...\n")

    time.sleep(60)