from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from selenium.webdriver.chrome.service import Service

def get_list(list_name):
    options = webdriver.ChromeOptions()
    service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox") 
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=service, options=options)
    url = f'https://open.spotify.com/search/{list_name}/playlists'

    driver.get(url)

    time.sleep(1)

    playlist_data = []
    i_list = []
    c = 0
    img = driver.find_elements(By.XPATH, '//img[contains(@data-testid, "card-image")]')
    for el in img :
        a = el.get_attribute('src')
        i_list.append(a)

    playlists = driver.find_elements(By.XPATH, '//div[@class = "Box__BoxComponent-sc-y4nds-0 kcRGDn Box-sc-1njtxi4-0 hscyXl aAYpzGljXQv1_zfopxaH Card"]')
    
    for el in playlists:
            try:
                aria_label = el.get_attribute('aria-labelledby')
                playlist_id = aria_label.split(':')[2].split('-')[0]

                title = driver.find_element(By.XPATH, f'//p[@id = "card-title-spotify:playlist:{aria_label.split(':')[2]}"]')
                subtitle = driver.find_element(By.XPATH, f'//div[@id="card-subtitle-spotify:playlist:{aria_label.split(':')[2]}"]/span/div/span')

                playlist_data.append([playlist_id,title.get_attribute('title'),subtitle.text,i_list[c]])
                c+= 1

            except Exception as e:
                print(f"Error processing playlist: {e}")
        
    driver.quit()

    return(playlist_data)

def export(data):
    with open ('/tmp/sub.html', 'w') as df:
        df.write(data)



if __name__ == '__main__':
    get_list('asd')
