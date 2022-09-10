from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
import bs4
import random

def now_time():
   now = datetime.datetime.now()
   return now.strftime('%m/%d %H:%M')+' '

username = input('username: ')
password = input('password: ')

tag = input('tag: ').split('\n')
tagName = random.choice(tag)
print(tagName)

#イイね数の設定
like = int(input('いいねする数: '))

from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome (ChromeDriverManager().install())

driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
print(now_time()+'instagramにアクセスしました')
time.sleep(1)

driver.find_element_by_name('username').send_keys(username)
time.sleep(1)
driver.find_element_by_name('password').send_keys(password)
time.sleep(1)

driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
time.sleep(2)
print(now_time()+'instagramにログインしました')
time.sleep(1)

#タグを検索
tag_search_url = 'https://www.instagram.com/explore/tags/'
driver.get(tag_search_url + tagName)
time.sleep(1)
print(now_time()+"指定のタグで検索しました")
time.sleep(3)


#直近で投稿ページに移動
target = driver.find_elements_by_class_name('_aagw')[10]
print(target)
actions = ActionChains(driver)
actions.move_to_element(target)
actions.perform()
print(now_time()+'最新の投稿に移動しました')
time.sleep(1)


#過去にイイねをしたか確認
def check_Like():
   html = driver.page_source.encode('utf-8')
   soup = bs4.BeautifulSoup(html, "html5lib")
   a = soup.select('span._aamw')
   return  not '取り消す' in str(a[0])


#直近の投稿にいいね
try:
   driver.find_elements_by_class_name('_aagw')[9].click()
   time.sleep(random.randint(3, 5))
   print(now_time()+'投稿をクリックしました')
   time.sleep(4)

   if check_Like():
       driver.find_element_by_class_name('_aamw').click()
       print(now_time()+'いいね(初回)')
       time.sleep(random.randint(3, 5))
   else:
       print(now_time()+'いいね済みのためスキップします')

except WebDriverException:
   print(now_time()+'エラーが発生しました')


#その他の投稿にイイねをしていく
for i in range(like-1):
   try:
       driver.find_element_by_xpath('//*[@class=" _aaqg _aaqh"]/button').click()
       print(now_time()+'次の投稿へ移動しました')
       time.sleep(random.randint(1, 3))
   except WebDriverException:
       print(now_time()+'{}つ目の位置でエラーが発生しました'.format(i+2))
       time.sleep(random.randint(2, 4))

   try:
       if check_Like():
           driver.find_element_by_class_name('_aamw').click()
           print(now_time()+'投稿をいいね({}回目)'.format(i+2))
           time.sleep(random.randint(1, 3))
       else:
           print(now_time()+'いいね済みのためスキップします')

   except WebDriverException:
       print(now_time()+'{}つ目の位置でエラーが発生しました'.format(i+3))


print(now_time()+'終了')
driver.close()
driver.quit()