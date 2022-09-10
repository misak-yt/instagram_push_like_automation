from re import U
from turtle import pu
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import bs4
import random

def now():
    now = datetime.datetime.now()
    return now.strftime('%m/%d %H:%M') + ' '

def access_and_login(driver, username, password):
    driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    print (now()+'instagramにアクセスしました')
    time.sleep(1)

    driver.find_element_by_name('username').send_keys(username)
    time.sleep(1)
    driver.find_element_by_name('password').send_keys(password)
    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
    time.sleep(2)
    print (now()+'instagramにログインしました')
    time.sleep(1)

#タグを検索
def tag_search(driver, tag_name):
    tag_search_url = 'https://www.instagram.com/explore/tags/'
    driver.get(tag_search_url + tag_name)
    time.sleep(1)
    print (now()+"指定のタグで検索しました")
    time.sleep(4)

#直近で投稿ページに移動
def move(driver, actions):
    target = driver.find_elements_by_class_name('_aagw')[10]
    print(target)
    actions = ActionChains(driver)
    actions.move_to_element(target)
    actions.perform()
    print (now()+'最新の投稿に移動しました')
    time.sleep(2)


#過去にイイねをしたか確認
def check_like(driver):
    html = driver.page_source.encode('utf-8')
    soup = bs4.BeautifulSoup(html, "html5lib") 
    a = soup.select('span._aamw')
    return  not 'いいねを取り消す' in str(a[0])

#直近の投稿にいいね
def push_like(driver, like):
    try:
        driver.find_elements_by_class_name('_aagw')[9].click()
        time.sleep(random.randint(2, 3))
        print (now()+'投稿をクリックしました')
        time.sleep(2)

        if check_like(driver):
            driver.find_element_by_class_name('_aamw').click()
            print (now()+'いいね(初回)')
            time.sleep(random.randint(2, 3))
        else:
            print (now()+'いいね済みのためスキップします')
    except WebDriverException: 
        print (now()+'エラーが発生しました')

    #その他の投稿にイイねをしていく
    for i in range(like - 1):
        try:
            driver.find_element_by_xpath('//*[@class=" _aaqg _aaqh"]/button').click()
            print (now() + '次の投稿へ移動しました')
            time.sleep(random.randint(1, 3))
        except WebDriverException:
            print (now() + '{}つ目の位置でエラーが発生しました'.format(i + 2))
            time.sleep(random.randint(2, 4))

        try:
            if check_like(driver):
                driver.find_element_by_class_name('_aamw').click()
                print (now() + '投稿をいいね({}回目)'.format(i + 2))
                time.sleep(random.randint(1, 3))
            else:
                print (now() + 'いいね済みのためスキップします')

        except WebDriverException:
            print (now() + '{}つ目の位置でエラーが発生しました'.format(i + 3))

def main():
    username = input('username: ')
    password = input('password: ')
    tag = input('tag: ').split('\n')
    tag_name = random.choice(tag)
    like = int(input('いいねする数: '))
    driver = webdriver.Chrome (ChromeDriverManager().install())
    actions = ActionChains(driver)

    access_and_login(driver, username, password)
    tag_search(driver, tag_name)
    move(driver, actions)
    push_like(driver, like)

    print (now()+'終了')
    driver.close()
    driver.quit()   


if __name__ == '__main__':
    main()
    