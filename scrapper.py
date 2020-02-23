from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import smtplib
import time
from tkinter import *
import sys

# tkinter gui for inputting user data
master = Tk()
Label(master, text='URL: ').grid(row=0)
Label(master, text='Email: ').grid(row=1)
Label(master, text='Original Price: ').grid(row=2)
e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)


# since data is not preserved unless saved, I place each of the user inputs into a global list
def getInput():
    a = e1.get()
    b = e2.get()
    c = e3.get()
    master.destroy()
    global params
    params = [a, b, c]


Button(master, text="sumbit", command=getInput).grid(row=3, sticky=W)
mainloop()

URL = params[0]
original_price = float(params[1])
og_email = params[2]

# test #s
# URL = 'https://www.amazon.com/PANASONIC-Megapixel-20-1200mm-Stabilization-DC-FZ80K/dp/B01MS16V42/ref
# =sxin_0_ac_d_rm?ac_md=0-0-ZHNscg%3D%3D-ac_d_rm&cv_ct_cx=dslr&keywords=dslr&pd_rd_i=B01MS16V42&pd_rd_r=7c792f2e-3984
# -4bfa-af6a-32d148777556&pd_rd_w=cz3uQ&pd_rd_wg=T5sLi&pf_rd_p=e2f20af2-9651-42af-9a45-89425d5bae34&pf_rd_r
# =NTRY2NS5WKHWKXJZDVJK&psc=1&qid=1577831160' original_price = 600 #297.99 #make user input??


"""
--------------------------------------------------------------------------------------------------
insert gmail account you wish to use to send emails here 
"""

MY_ADDRESS = 'pythondev242@gmail.com'
PASSWORD = 'password to email here'

"""
--------------------------------------------------------------------------------------------------
"""


# Checks price of item on Amazon using Selenium and geckodriver since there's javascript
def checkprice():
    # it is possible to make firefox headless programmatically using selenium by below steps
    options = Options()
    options.headless = True
    # if you want to use chrome use the commented line below
    # driver = webdriver.Chrome(options=options,
    # executable_path='/Users/benjaminpasternak/Desktop/python projects/chromedriver-1')
    driver = webdriver.Firefox(options=options,
                               executable_path='/Users/benjaminpasternak/Desktop/python projects/geckodriver')

    driver.get(URL)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # prodTitle = soup.find(id="productTitle").getText()
    price = soup.find(id="priceblock_ourprice").get_text()

    driver.quit()

    priceInt = float(price[1:])
    if priceInt < original_price:
        send_mail()
        sys.exit()


# sends the email to user using the gmail smtp server and port 587 (standard)
def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(MY_ADDRESS, PASSWORD)
    subject = 'Price fell down'
    body = 'check your link : ' + URL
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(MY_ADDRESS, og_email, msg)
    print('EMAIL HAS BEEN SENT')
    server.quit()


# program continues to run until terminated or price is reduced
# checking daily to see if the price is reduced, can be changed to weekly by *7
while True:
    checkprice()
    time.sleep(60 * 60 * 24)
