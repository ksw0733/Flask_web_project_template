from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib.request
import time

def animeGAN(src_fname, version):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')   # 화면없이 실행
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-infobars')
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome('chromedriver', options=options)

    url = 'https://huggingface.co/spaces/akhaliq/AnimeGANv2'
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get(url)
    time.sleep(5)

    # iframe 전환
    driver.switch_to.frame('iFrameResizer0')
    # 이미지 업로드
    upload = driver.find_element(By.CSS_SELECTOR, 'input.hidden-upload.hidden')
    upload.send_keys('C:\\Workspace\\02.FirstProject\\static\\upload\\'+src_fname)
    time.sleep(1)

    # 제출하기 버튼 클릭
    button = driver.find_element(By.CSS_SELECTOR, 'button.gr-button.gr-button-lg.gr-button-primary.self-start')
    button.click()
    time.sleep(5)

    ani_img = driver.find_element(By.XPATH, '//*[@id="2"]/img')
    img_url = ani_img.get_attribute('src')
    urllib.request.urlretrieve(img_url, "animated_image.jpg")

    driver.close()