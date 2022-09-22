import smtplib
import time
from email.message import EmailMessage
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from jinja2 import Environment,FileSystemLoader, select_autoescape
template_env = Environment(
    loader = FileSystemLoader("template"),
    autoescape=select_autoescape()
)
foundConcerts, prevFoundConcerts={},{}
artists = {
    "The_Weeknd": "https://www.theweeknd.com/tour",
    "Florence":"https://florenceandthemachine.net",
    "Remi_Wolf":"https://remiwolf.com/pages/tour",
    "Polica":"https://www.thisispolica.com/tour",
    "Sharon": "https://www.sharonvanetten.com/tour",
    "Alice_Lou": "https://www.alicephoebelou.com/concerts.php"
}
desired_locations = ["Durham","Raleigh","Baltimore","Richmond","Los Angeles"]
WAIT_TIME = 86400

def sendEmail(email_body):
    msg = EmailMessage()
    msg.set_content(email_body)
    msg.add_alternative(email_body, subtype='html')
    msg['Subject'] = 'Concert(s) You May Be Interested In'
    msg['From'] = gmail_user
    msg['To'] = gmail_user

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.send_message(msg)
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)
 

def findConcerts(artist,url,driver):
    driver.get(url)
    tourPage = driver.page_source
    soup = BeautifulSoup(tourPage, 'html.parser')
    links = soup.find_all('a')
    spans = soup.find_all('span')
    divs = soup.find_all('div')

    for link in links:
        for location in desired_locations:
            if location.lower() in link.text.lower():
                foundConcerts[artist] = {"location": location,"url":url}
                return

    for span in spans:
        for location in desired_locations:
            if location.lower() in span.text.lower():
                foundConcerts[artist] = {"location": location,"url":url}
                return

    for div in divs:
        for location in desired_locations:
            if location.lower() in div.text.lower():
                foundConcerts[artist] = {"location": location,"url":url}
                return

def main():
    browser_driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
    for artist in artists:
        findConcerts(artist,artists[artist],browser_driver)
    browser_driver.quit() 
    template = template_env.get_template("./emailtemplate.html")

    #Python ¯\_(ツ)_/¯ 
    global prevFoundConcerts, foundConcerts

    #Easiest safe-guard I could come up with to avoid sending the same emails every runtime            
    if len(foundConcerts) > 1 and len(foundConcerts) != len(prevFoundConcerts):
        sendEmail(template.render(concerts=foundConcerts))
       
    prevFoundConcerts = foundConcerts.copy()
    foundConcerts.clear()  


if __name__ == '__main__':
    gmail_user = input("Enter your email and press enter: ")
    gmail_password = input("Enter your password and press enter: ")
    print("========Scraping in progress=========")
    while True:
        main()
        time.sleep(WAIT_TIME)#wait for 24hrs before runnning again