from keys import email, password
import requests
from bs4 import BeautifulSoup
import smtplib
import time

URL = 'https://www.amazon.in/Targus-KB55-Multi-Platform-Bluetooth-Keyboard/dp/B07C7VCTJH/ref=sr_1_5?dchild=1&keywords=bluetooth+keyboard&qid=1606309738&sr=8-5'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36"
}


def checkPrice():
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find(id='productTitle').getText().strip()
    rawPrice = soup.find(id='priceblock_ourprice').getText()
    price = float(rawPrice[2:7].replace(',', ''))
    print(title, price)

    if price <= 900:
        sendEmail(price)


def sendEmail(price):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email, password)

    subject = 'Bluetooth keyboard price fell down!'
    body = f'Now Price is : {price} \n Check amazon link https://www.amazon.in/Targus-KB55-Multi-Platform-Bluetooth-Keyboard/dp/B07C7VCTJH/ref=sr_1_5?dchild=1&keywords=bluetooth+keyboard&qid=1606309738&sr=8-5'

    msg = f'Subject:{subject}\n\n{body}'

    server.sendmail(
        email,
        'vedant.debadwar@gmail.com',
        msg
    )

    print('Email has been sent.')
    server.quit()


while True:
    checkPrice()
    time.sleep(60*60*6)
