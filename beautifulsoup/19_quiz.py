# Quiz) 부동산 매물(송파 헬리오시티) 정보를 스크래핑 하는 프로그램을 만드시오

# [조회 조건]
# 1. http://daum.net 접속
# 2. '송파 헬리오시티' 검색
# 3. 다음 부동산 부분에 나오는 결과 정보

# [출력 결과]
# ========== 매물 1 ==========
# 거래 : 매매
# 면적 : 84/59
# 가격 : 165,000 (만원)
# 동 : 214동
# 층 : 고/23
# ========== 매물 2 ==========
#     ...

# [주의 사항]
# - 실습하는 시점에 위 매물이 없다면 다른 곳으로 대체 가능

 # 유튜브 튜토리얼의 코딩 (업로드 당일에는 미세먼지 항목이 포함되어 있었음)

# import os
# import requests
# from bs4 import BeautifulSoup

# url = "https://search.daum.net/search?nil_suggest=btn&w=tot&DA=SBC&q=%EC%86%A1%ED%8C%8C+%ED%97%AC%EB%A6%AC%EC%98%A4%EC%8B%9C%ED%8B%B0"
# res = requests.get(url)
# res.raise_for_status()
# soup = BeautifulSoup(res.text, "lxml")

# os.chdir("C:/Users/hooni/Documents/coding/nadocoding/4_webscraping_basic")
# with open("19_quiz.html", "w", encoding="utf8") as f:
#     f.write(soup.prettify())

# data_rows = soup.find("table", attrs={"class":"tbl"}).find("tbody").find_all("tr")
# for index, row in enumerate(data_rows):
#     columns = row.find_all("td")

#     print("========== 매물 {} ==========".format(index+1))
#     print("거래 : ", columns[0].get_text().strip())
#     print("면적 : ", columns[1].get_text().strip(), "(공급/전용)")
#     print("가격 : ", columns[2].get_text().strip(), "(만원)")
#     print("동 : ", columns[3].get_text().strip())
#     print("층 : ", columns[4].get_text().strip())


######################################################

# 다음 부동산 매물 이 더이상 제공 안하는 관계로 역대 EPL 시즌 결과를 사용

# [조회 조건]
# 1. https://en.wikipedia.org/wiki/List_of_Premier_League_seasonst 접속
# 2. 'List of Premier League seasons' 검색
# 3. 나오는 결과 정보 조회

# [출력 결과]
# ========== 시즌 xxxx-xx ==========
# 1. 우승팀 : ...
# 2. 챔스진출팀 : ...
# 3. 유로파진출팀 : ...
# 4.강등팀 : ...
# 5. 승격팀 : ...
# 6. 골든부츠 : ...
# 7. 골 수 : ...
# ========== 시즌 xxxx-xx ==========
#     ...

# import os
import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/List_of_Premier_League_seasons"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
res = requests.get(url, headers=headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")

data_rows = soup.find("table", attrs={"class":"wikitable sortable"}).find("tbody").find_all("tr")[2:] # 3 번째 줄부터 (1,2 번째는 thead)
# print(data_rows)

for index, row in enumerate(data_rows):
    columns = row.find_all("td")
    
    # 팀 사이에 일정거리(탭) 으로 구분 짓기, a tag 없애기 ([]로 적혀 있는 부분)
    year = row.find("th").get_text().strip()
    champions = columns[0].get_text().strip()
    champions_league = columns[1].get_text("\t").strip()
    europa_league = columns[2].get_text("\t").strip()
    relegated = columns[3].get_text("\t").strip()
    promoted = columns[4].get_text("\t").strip()
    top_goal_scorer = columns[5].get_text("\t").strip()
    goals_in_PL = columns[6].get_text("\t").strip()

    print()
    print("{}. ======================= Season {} =======================".format(index+1, year))
    print("Champions :", champions)
    print("Champions League :", champions_league)
    print("UEFA Cup/Europa League :", europa_league)
    print("Relegated :", relegated)
    print("Promoted :", promoted)
    print("Top Goal Scorer :", top_goal_scorer)
    print("Goals in PL :", goals_in_PL)
    # print(columns)

# 출력 확인
# os.chdir("C:/Users/hooni/Documents/coding/nadocoding/4_webscraping_basic")
# with open("19_quiz.html", "w", encoding="utf8") as f:
#     f.write(soup.prettify())