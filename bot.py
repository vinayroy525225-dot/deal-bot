import requests
from bs4 import BeautifulSoup
import time

BOT_TOKEN = "8622451849:AAFl4jjC2mr5rf2671SA3F4g3vIFcqEYwGs"
CHAT_ID = "5044500645"

URL = "https://www.amazon.in/Oppo-K13-5G-Prism-Storage/dp/B0F8W2D943/522-6651414-9906254?pd_rd_w=cFCWN&content-id=amzn1.sym.d1406b44-aa69-47e4-9270-f613e12d52dc&pf_rd_p=d1406b44-aa69-47e4-9270-f613e12d52dc&pf_rd_r=F94RZH9YNVERVG9K292M&pd_rd_wg=kUT2o&pd_rd_r=33bea165-9c6e-4265-8fef-87d9a69fa1e2&pd_rd_i=B0F8W2D943&psc=1"

TARGET_PRICE = 18500

headers = {
    "User-Agent": "Mozilla/5.0"
}

while True:

    print("Checking Price...")

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")

    price = soup.find("span", class_="a-price-whole")

    if price:

        current_price = int(price.text.replace(",", "").replace(".", ""))

        print("CURRENT PRICE:", current_price)

        if current_price <= TARGET_PRICE:

            message = f"🔥 Deal Alert!\nPrice: ₹{current_price}\n{URL}"

            send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

            data = {
                "chat_id": CHAT_ID,
                "text": message
            }

            requests.post(send_url, data=data)

            print("TELEGRAM ALERT SENT")

        else:
            print("Price Still High")

    else:
        print("Price Not Found")

    print("Checking again in 60 sec...\n")

    time.sleep(60)