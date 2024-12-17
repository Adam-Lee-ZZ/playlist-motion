from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def get_list(list_name):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) 
    url = f'https://open.spotify.com/search/{list_name}/playlists'

    p_list = []
    i_list = []
    n_list = []
    c_list = []
    ll = []

    driver.get(url)
    time.sleep(1)
    l = driver.find_elements(By.XPATH,'//div[@class = "Box__BoxComponent-sc-y4nds-0 kcRGDn Box-sc-1njtxi4-0 hscyXl aAYpzGljXQv1_zfopxaH Card"]')
    for el in l :
        a = el.get_attribute('aria-labelledby').split(':')[2]
        p_list.append(a.split('-')[0])
        n = driver.find_element(By.XPATH, f'//p[@id = "card-title-spotify:playlist:{a}"]')
        c = driver.find_element(By.XPATH, f'//div[@id="card-subtitle-spotify:playlist:{a}"]/span/div/span')
        n_list.append(n.get_attribute('title'))
        c_list.append(c.text)

    img = driver.find_elements(By.XPATH, '//img[contains(@data-testid, "card-image")]')
    for el in img :
        a = el.get_attribute('src')
        i_list.append(a)

    for i in range(len(p_list)):
        ll.append([p_list[i],i_list[i],n_list[i],c_list[i]])
    
    ll = pd.DataFrame(ll,columns=["playlist_url",'image_src',"playlist_name","creater"])
    driver.quit()


    return(ll)

def export(data):
    with open ('/Users/adamlee/Desktop/music/Templates/sub.html', 'w') as df:
        df.write(data)



if __name__ == '__main__':
    get_list('asd')
