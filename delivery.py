import requests
import json
import bs4
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

#PATH = "C:/Users/96103/Desktop/lineBot/msedgedriver.exe"

def foodpanda_city_rest(city):
    city_dict = {
        '臺北市':'taipei-city',
        '新北市':'new-taipei-city',
        '基隆市':'keelung',
        '臺中市':'taichung-city',
        '高雄市':'kaohsiung-city',
        '桃園市':'taoyuan-city',
        '新竹市':'hsinchu-city',
        '臺南市':'tainan-city',
        '苗栗縣':'miaoli-county',
        '彰化縣':'changhua',
        '南投縣':'nantou-county',
        '雲林縣':'yunlin-county',
        '嘉義縣':'chiayi-city-jia-yi-shi',
        '屏東縣':'pingtung-city',
        '宜蘭縣':'yilan-city',
        '花蓮縣':'hualien',
        '臺東縣':'taitung-county',
        '澎湖縣':'penghu-city',
        '金門縣':'kinmen-city'
    }
    url = f"https://www.foodpanda.com.tw/city/{city_dict[city]}"
    header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    session = requests.Session()
    r = session.get(url, headers = header)
    content = r.text
    soup = bs4.BeautifulSoup(content, "html.parser")
    print(soup)

    titles = soup.find_all("span", class_="name fn")
    images = soup.find_all("div", class_="vendor-picture b-lazy")
    infoUrl = soup.find_all("a", class_="hreview-aggregate url")

    result = []
    titleName = []
    shopImage = []
    shopInfoUrl = []

    for title in titles:
        if title.get_text() != None:
            titleName.append(title.get_text())

    for image in images:
        shopImage.append(image["data-src"].split("|")[1])

    for url in infoUrl:
        shopInfoUrl.append(url["href"])

    for i in range(0, len(titleName)):
        input_dict = {'title':titleName[i], 'image':shopImage[i], 'infoUrl':shopInfoUrl[i]}
        result.append(input_dict)

    return eval(json.dumps(result, ensure_ascii=False))

def foodpanda_location_rest(location,scrollCount=5,debug=False):
    """
    :param location: 地點
    :param scrollCount: 滾動次數
    :return:dict[rest_name] rest_link
    """
    driver = webdriver.Safari()
    rest = dict()
    url = f"https://www.foodpanda.com.tw/restaurants/new?lat={location[0]}&lng={location[1]}&vertical=restaurants"
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    for _ in range(scrollCount):
        sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    vendor_list = driver.find_element(by=By.CLASS_NAME, value="vendor-list")
    datas = vendor_list.find_elements(by=By.CLASS_NAME, value='vendor-tile-wrapper')
    for i,data in enumerate(datas):
        rest_name = rest_name_proc(data.find_element(by=By.XPATH, value=f'//*[@id="restaurant-listing-root"]/div/div[3]/div/main/div[3]/section/ul/li[{i+1}]/a/figure/figcaption/span/span[1]').text)
        rest_link = data.find_element(by=By.XPATH, value=f'//*[@id="restaurant-listing-root"]/div/div[3]/div/main/div[3]/section[1]/ul/li[{i+1}]/a').get_attribute("href")
        rest[rest_name] = rest_link
        if debug:
            print(f"[&foodpanda_location_rest Debug] 店名：{rest_name} 連結：{rest_link}")
    driver.quit()
    return rest

def rest_name_proc(rest_name):
    try:
        rest_name = rest_name.replace(' ','')
        rsite = rest_name.index('(')
        return rest_name[:rsite]
    except:
        return rest_name.replace(' ','')

if __name__ == "__main__":
    data = foodpanda_location_rest([23.7043495, 120.4264846])