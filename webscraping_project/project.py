import os
import re
import requests
from bs4 import BeautifulSoup

# url 불러오기
def create_soup(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml")
    return soup

# 번호랑 같이 출력하기
def print_news(index, title, link):
    print("{}. {}".format(index+1, title))
    print("    (링크: {})".format(link))


# [오늘의 날씨]
# 흐림, 어제보다 00 높아요
# 현재 00 (최저 00 / 최고 00)
# 오전 강수확률 00% / 오후 강수확률 00%

# 미세먼지 00 좋음
# 초미세먼지 00 좋음
def scrape_weather():
    print("[오늘의 날씨]")
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%84%9C%EC%9A%B8+%EB%82%A0%EC%94%A8"
    soup = create_soup(url)

    # 출력확인
    # os.chdir("C:/Users/hooni/Documents/coding/nadocoding/4_webscraping_basic/webscraping_project")
    # with open("project.html", "w", encoding="utf8") as f:
    #     f.write(soup.prettify())

    # 흐림, 어제보다 00 높아요
    cast = soup.find("div", attrs={"class":"temperature_info"}).get_text().strip() # strip() 으로 맨 앞 여백 없애기
    # 현재 00 (최저 00 / 최고 00)
    curr_temp = soup.find("div", attrs={"class":"temperature_text"}).get_text().strip()
    min_temp = soup.find("span", attrs={"class":"lowest"}).get_text() # 최저 온도
    max_temp = soup.find("span", attrs={"class":"highest"}).get_text() # 최고 온도
    # 오전 강수확률 00% / 오후 강수확률 00%
    morning_rain_rate = soup.find("span", attrs={"class":"rainfall"}).get_text() # 오전 강수확률
    morning_rain_rate = soup.find("span", attrs={"class":"weather_left"}).get_text() # 오전 강수확륙 시도

    # 미세먼지 00 좋음
    # 초미세먼지 00 좋음
    # 예시
    # dust = soup.find("dl", attrs={"class":["indicator", "class2"], "id":"dust"}, text=["미세먼지", "초미세먼지"])
    # 유튜브 튜토리얼의 코딩 (업로드 당일에는 미세먼지 항목이 포함되어 있었음)
    # dust = soup.find("dl", attrs={"class":"indicator"})
    # pm10 = dust.find.all("dd")[0].get_text() # 미세먼지. dd 에 해당된 0번째 텍스트 가져오기
    # pm25 = dust.find.all("dd")[1].get_text() # 초미세먼지. dd 에 해당된 1번째 텍스트 가져오기
    
    # [현재(2022.02.05) 네이버 포맷 변경] 미세먼지 항목이 사라져서 자외선, 일몰로 대체
    today_chart_list = soup.find("div", attrs={"class":"report_card_wrap"}).get_text().strip() # 미세먼지, 초미세먼지, 자외선, 일몰

    # 출력
    # 어제보다 1° 높아요  맑음   강수확률 0% 습도 31% 바람(서풍) 2m/s
    print(cast)
    # 현재 온도1°  (최저기온-7° / 최고기온4°)
    print("{} ({} / {})".format(curr_temp, min_temp, max_temp))
    # 미세먼지 좋음, 초미세먼지 좋음, 자외선 좋음, 일몰 17:57
    # print("미세먼지 {}".format(pm10)
    # print("초미세먼지 {}".format(pm25))
    print(today_chart_list)
    print()
    

# [헤드라인 뉴스]
# 1. 무슨 무슨 일이...
# (링크 : https://...)
# 2. 무슨 무슨 일이...
# (링크 : https://...)
# 3. 무슨 무슨 일이...
# (링크 : https://...)
def scrape_headline_news():
    print("[헤드라인 뉴스]")
    url = "https://news.naver.com/"
    soup = create_soup(url)
    # 유튜브 튜토리얼의 코딩 (업로드 당일에는 미세먼지 항목이 포함되어 있었음)
    # news_list = soup.find("ul", attrs={"class":"hdline_article_list"}).find_all("li",limit=3)
    # for index, news in enumerate(news_list):
    #     title = news.find("a").get_text().strip()
    #     link = url + news.find("a")["href"]
    #     print("{}. {}".format(index+1, title))
    #     print("    (링크: {})".format(link))
    # print()
    
    news_list = soup.find_all("div", attrs={"class":"cjs_journal_wrap _item_contents"}, limit=3) # find_all() 은 find() 안에서 부를 수 있지만 반대는 안됌. limit 은 find_all() 에서만 가능
    # print(news_list) html 값 확인
    for index, news in enumerate(news_list):
        title = news.find("div", attrs={"class":"cjs_t"}).get_text()
        link = news.find("a")["href"]
        print_news(index, title, link)
    print()


# [IT 뉴스]
# 1. 무슨 무슨 일이...
# (링크 : https://...)
# 2. 무슨 무슨 일이...
# (링크 : https://...)
# 3. 무슨 무슨 일이...
# (링크 : https://...)
def scrape_it_news():
    print("[IT 일반 뉴스]")
    url = "https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=105&sid2=230"
    soup = create_soup(url)
    
    news_list = soup.find("ul", attrs={"class":"type06_headline"}).find_all("li", limit=3)
    for index, news in enumerate(news_list):
        a_idx = 0
        img = news.find("img")
        if img:
            a_idx = 1 # img 태그가 있으면 1번째 a 태그의 정보를 사용

        a_tag = news.find_all("a")[a_idx]
        title = a_tag.get_text().strip()
        link = a_tag["href"]
        print_news(index, title, link)
    print()


# [오늘의 영어 회화]
# (영어 지문)
# Jason : How do you think bla bla?
# Kim : Well, I think ...

# (한글 지문)
# Jason : 어쩌구 저쩌구 어떻게 생각하세요?
# Kim : 글쎄요, 저는 어쩌구 저쩌구
def scrape_english():
    print("[오늘의 영어 회화]")
    url = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english&keywd=haceng_submain_lnb_eng_I_others_english&logger_kw=haceng_submain_lnb_eng_I_others_english"
    soup = create_soup(url)
    sentences = soup.find_all("div", attrs={"id":re.compile("^conv_kor_t")})
    # 출력 확인
    # print(sentences)
    # print(len(sentences))
    
    print("(영어 지문)")
    for sentence in sentences[len(sentences)//2:]: # 8문장이 있다고 가정할 때, 5~8(index 기준 4~7) 까지 잘라서 가져옴. len(sentences) = 8 나누기 2 를 한 것 부터 끝까지. // 2개인 이유는 만약에 7같은 홀수가 있을때 정수로 바꿔서 출력 하기 위해
        print(sentence.get_text().strip())
    print()

    print("(한글 지문)")
    for sentence in sentences[:len(sentences)//2]: # 8문장이 있다고 가정할 때, index 기준 0~3 까지 잘라서 가져옴
        print(sentence.get_text().strip())
    print()


if __name__ == "__main__": # 이 프로젝트를 직접 실행할때만 동작할거고 다른 파일에 의해서 호출 될 땐 실행이 안됌
    scrape_weather() # 오늘의 날씨 정보 가져오기
    scrape_headline_news() # 헤드라인 뉴스 정보 가져오기
    scrape_it_news() # IT 일반 뉴스 정보 가져오?기
    scrape_english() # 오늘의 영어 회화 가져오기