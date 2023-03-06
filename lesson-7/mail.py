from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time

client = MongoClient('localhost', 27017)
emails = client['emails']
mailru = emails.mail
driver = webdriver.Chrome()

driver.get('https://mail.ru/')
assert "Mail.ru: почта, поиск в интернете, новости, игры" in driver.title
mail_box = []

elem = driver.find_element_by_id('mailbox:login')
elem.send_keys('study.ai_172')
button = driver.find_element_by_xpath('//input[@class="o-control"]')
button.click()
driver.implicitly_wait(5)
elem = driver.find_element_by_xpath('//input[@id="mailbox:password"]')
elem.send_keys('Password172')
button = driver.find_element_by_xpath('//input[@class="o-control"]')
button.send_keys(Keys.RETURN)
time.sleep(7)
#button = driver.find_element_by_class_name('o-control')

assert "Входящие" in driver.title
driver.implicitly_wait(10)

def read_mail(mail):
    #driver.get('https://e.mail.ru/inbox/?back=1&afterReload=1')
    i = 0
    email = {}
    while i < 1: #len(all_mails):
        driver.implicitly_wait(10)
        mail = mail
        print('mail', mail)
        # mail_id = driver.get(mail.get_attribute('href'))
        mail.send_keys(Keys.RETURN)
        #mail.click()
        time.sleep(5)

        assert "Почта Mail.ru" in driver.title

        driver.implicitly_wait(5)
        url = driver.current_url
        print('url', url)
        driver.get(url)
        #mail_id = url.split(':')[2]
        #print(mail_id)
        header = driver.find_element_by_xpath('//h2').text

        print(header)
        sender = driver.find_element_by_xpath('//span[@class="letter__contact-item"]').get_attribute('title')
        print(sender)
        mail_time = driver.find_element_by_xpath('//div[@class="letter__date"]').text
        print(mail_time)
        # text_route = f'//div[@id="style_{mail_id}_BODY"]'
        text_route = '//div[@class="letter-body__body"]'
        print(text_route)
        # text = driver.find_element_by_xpath('//div[@id="letter__date"]/text()')
        text = driver.find_element_by_xpath(text_route).text
        email['header'] = header
        email['time'] = mail_time
        email['sender'] = sender
        email['text'] = text
        #email['text2'] = mail.text

        #mail_box.append(email)
        print(text)
        #print(mail.text)

        i += 1
        driver.back()
        return email
i = 0
all_mails = driver.find_elements_by_xpath('//a[@class="llc js-tooltip-direction_letter-bottom js-letter-list-item llc_normal"]')
print('len: ' + str(len(all_mails)))
print(all_mails)



while True:

    print(i,  len(all_mails))

    mail_box.append(read_mail(all_mails[i]))
    mailru.insert_one(read_mail(all_mails[i]))
    all_mails = driver.find_elements_by_xpath(
        '//a[@class="llc js-tooltip-direction_letter-bottom js-letter-list-item llc_normal"]')
    #element = all_mails[i]
    #actions = ActionChains(driver)
    #actions.move_to_element(element).perform()

    if i>15:
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        for h in range(1, i%15 +2):
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            all_mails = driver.find_elements_by_xpath(
                '//a[@class="llc js-tooltip-direction_letter-bottom js-letter-list-item llc_normal"]')

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    i += 1
print(mail_box)
driver.quit()
