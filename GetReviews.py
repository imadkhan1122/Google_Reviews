import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import urllib
import requests
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time
from lxml import etree
from selenium.common.exceptions import TimeoutException

def GET_REVIEWS(str_):   
    import undetected_chromedriver as uc
    URL = 'https://www.google.com/maps/'
    links = []
    options = Options()
    # prefs = {"profile.default_content_setting_values.geolocation" :2}
    # options.add_experimental_option("prefs",prefs)
    # options.add_argument('--headless')
    # open chrome browser
    driver = uc.Chrome(options=options)
    # Go to given URL
    driver.get(URL)
    # wait for 5 seconds
    delay = 10 # seconds
    
    while True:
        time.sleep(5)
        openbtn = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#searchboxinput')))
        btn = openbtn.send_keys(str_)
        time.sleep(1)
        btn = driver.find_element(By.ID, 'searchbox-searchbutton')
        # clr = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Clear search"]')
        # print(clr)
        time.sleep(3)
        btn.click()
        break
    time.sleep(0.02)
    actions = ActionChains(driver)
    ele = ''
    while True:  
        actions.send_keys(Keys.DOWN).perform()
        try:
            element = driver.find_element(By.CSS_SELECTOR, 'span[jsan="7.HlvSq,5.color"]')
            ele = element.text
            print(ele)
        except:
            ele = ''
        time.sleep(0.02)
        if ele == '''You've reached the end of the list.''':
            break
    LNKS = []
    links = driver.find_elements(By.TAG_NAME, 'a')
    for lnk in links:
        url = lnk.get_attribute('href')
        if url not in LNKS:
            try:
                base_url = os.path.split(url)[0]
                if  base_url.split('/')[-1] == str_.split(',')[0]:
                    LNKS.append(url)
            except:
                pass        
    time.sleep(5)
    driver.quit()
    
    return LNKS

def GET_FIELDS(query):

    query = 'Starbucks, WV, US'
    Link = GET_REVIEWS(query)
    ReViewerTxt = [] 
    Query = query.split(' ')
    url = Link[20]
    URL = []
    Name = '' 
    try:
        base_url = os.path.split(url)[0]
        if  base_url.split('/')[-1] == query.split(',')[0]:
            Name = base_url.split('/')[-1]
            URL.append(url)
    except:
        pass
    google_id = ''
    place_id  = ''
    Reviews_Link = """https://search.google.com/local/reviews?placeid="""+place_id+"""&q="""+Query[0]+'+'+Query[1]+'+'+Query[-1]+"""&authuser=0&hl=en&gl=US"""
    for i in URL[0].split('!'):
        if i.startswith('1s'):
            google_id = i[2:]
        if i.startswith('19s'):
            place_id = i[3:i.index('?')]
    import undetected_chromedriver as uc
    options = Options()
    # options.add_argument("--start-maximized")
    # options.add_argument('--headless')
    # open chrome browser
    driver = uc.Chrome(options=options)
    # Go to given URL
    driver.get(url)
    # wait for 5 seconds
    delay = 10 # seconds
    action = ActionChains(driver)
    while True:
        time.sleep(5)
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[id="searchbox-searchbutton"]')))
        ele = driver.find_element(By.CSS_SELECTOR, 'div.PPCwl')
        action.move_to_element(ele).click().perform()
        break
    
    time.sleep(0.02)
    SCROLL_PAUSE_TIME = 5
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    number = 0
    
    while True:
        number = number+1
        # Scroll down to bottom 
        ele = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')
        driver.execute_script('arguments[0].scrollBy(0, 5000);', ele)
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        print(f'last height: {last_height}')
        ele = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')
        new_height = driver.execute_script("return arguments[0].scrollHeight", ele)
        print(f'new height: {new_height}')
        if new_height == last_height:
            break
        print('cont')
        last_height = new_height
    
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    rat_table = soup.find('div', class_='PPCwl')
    rating_sec = rat_table.find('div', class_='jANrlb')
    rating_reviews = rating_sec.text.strip().split()
    Rating = rating_reviews[0]
    Reviews = rating_reviews[1]
    Reviews_Per_Score = {}
    tbl = rat_table.find('table')
    for tr in tbl.find_all('tr'):
        SPR = tr["aria-label"].split(',')
        Reviews_Per_Score.update({SPR[0].split(' ')[0]:SPR[1].strip().split(' ')[0]})
    
    # ReViewerData = driver.find_element(By.XPATH, '/html[1]/body[1]/div[3]/div[9]/div[9]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[9]')
    ReViewerText = driver.find_elements(By.XPATH, '/html[1]/body[1]/div[3]/div[9]/div[9]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[9]/div')                                               
    for txt in ReViewerText:
        if txt.text != '':
            txt1 = txt.text.split('\n')
            Author_Title = txt1[0]
            Auther_No_Of_Reviews = txt1[1]
            try:
                Review_Rating = txt.find_element(By.CSS_SELECTOR, 'span.kvMYJc').get_attribute('aria-label')
            except:
                Review_Rating = ''
            try:
                Review_Text = txt.find_element(By.CSS_SELECTOR, 'span.wiI7pd').text
            except:
                Review_Text = ''
            try:
                Owner_Response = txt.find_element(By.CSS_SELECTOR, 'div.wiI7pd').text
            except:
                Owner_Response = ''
            try:
                Review_Likes = txt.find_element(By.CSS_SELECTOR, 'span.znYl0').text
            except:
                Review_Likes = ''
            if Review_Likes == 'Like' or Review_Likes == '':
                Review_Likes = 0  
            Auther_Link = txt.find_element(By.TAG_NAME, 'a').get_attribute('href')
            Auther_Id = Auther_Link[Auther_Link.find('contrib/')+len('contrib/'):Auther_Link.rfind('/reviews')]
            Auther_Image = txt.find_element(By.TAG_NAME, 'img').get_attribute('src')
            Review_Image_Urls = ''
            try:
                Images = txt.find_elements(By.TAG_NAME, 'button')
                imgLink = [i.get_attribute('style') for i in Images if 'background-image:' in i.get_attribute('style')]
                Review_Image_Urls = [s[s.index("(")+2:s.index(")")-1] for s in imgLink if s!='']
            except:
                Review_Image_Urls = ''
            LST = [query, Name, google_id, place_id, Reviews_Link, Rating, Reviews, Reviews_Per_Score
                   , Author_Title, Auther_No_Of_Reviews, Review_Rating, Review_Text, Review_Likes,
                   Auther_Link, Auther_Id, Auther_Image, Review_Image_Urls]
            ReViewerTxt.append(LST) 
    driver.quit()
    return ReViewerTxt