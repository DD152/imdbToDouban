import os
import pandas

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login():
    mydriver = webdriver.Edge()
    mydriver.get('https://accounts.douban.com/passport/login?source=main')
    login_url = mydriver.current_url
    while True:
        WebDriverWait(mydriver, 600, 0.5, EC.url_changes(login_url))
        if mydriver.current_url == 'https://www.douban.com/':
            break

    print("login successful")
    return mydriver


def importIMDB(constNumber):
    mydriver = login()
    for tt in constNumber:
        mydriver.get('https://www.douban.com/search?source=suggest&q=' + tt)

        mydriver.get(
            mydriver.find_element(By.CLASS_NAME, 'title').find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))
        movieUrl = mydriver.current_url
        doubanMovieID = movieUrl.split('/')[-2]
        WebDriverWait(mydriver, 10).until(EC.presence_of_element_located((By.ID, 'interest_sect_level')))
        try:
            WebDriverWait(mydriver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, 'mr10')))
            print(tt + " already collect")
        except Exception as e:
            xiangkanButton = 'pbtn-' + doubanMovieID + '-collect'
            mydriver.find_element(By.ID, 'interest_sect_level').find_element(By.NAME, xiangkanButton).click()
            submit = WebDriverWait(mydriver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'interest-form-ft')))
            submit.find_element(
                By.CSS_SELECTOR, 'span').find_element(By.CSS_SELECTOR, 'input').click()
            WebDriverWait(mydriver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'mr10')))
            print(tt + " collect")


if __name__ == '__main__':
    file_name = os.path.dirname(os.path.abspath(__file__)) + '/WATCHLIST.csv'
    rowCosnt=pandas.read_csv(file_name,usecols=['Const'])
    rowtt=rowCosnt.values.tolist()
    tt=[token for items in rowtt for token in items]
    # 将imdb tt编号list传入importIMDB()
    importIMDB(tt)
