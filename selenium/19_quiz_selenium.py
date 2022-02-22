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

######################################################

# 1. https://new.land.naver.com/complexes 네이버 부동산 매물 접속
# 2. '제주 외도1동 부영2차
# 3. 전체 거래 결과 정보 조회 및 출력

import time
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import csv


# selenium setup
browser = webdriver.Chrome()
browser.maximize_window()

url = "https://new.land.naver.com/complexes"
browser.get(url)
time.sleep(5)


# 부동산 매물 검색
browser.find_element_by_class_name("search_input").send_keys("한남동 한남더힐")
browser.find_element_by_class_name("button_search--icon").click()
time.sleep(5)

# 매물 찾기
items = browser.find_elements_by_class_name("item_link")[:5] # 매물들을 리스트로 만들어서 처음 5개까지 찾기
time.sleep(5)


# 부동산 매물 csv 파일로 저장하기
os.chdir("C:/Users/hooni/Documents/coding/nadocoding/4_webscraping_basic")

filename = "19_quiz_selenium.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="") # 자동 줄 바꿈 없애기 위해 newline 은 공백으로. excel 에서 열 때 encoding="utf-8-sig" 로 설정 utf8 은 텍스트 파일에서만 한글이 안 깨지게 함
writer = csv.writer(f) # 파일이 열러있는지 확인. 열려있으면 ERROR: Permission denied 

# 밑 내용은 데이터를 가져올때 테이블 형식 그대로 가져오기 때문에 불필요
# # csv 파일안에 first columns 설정하기 ["N", "종목명", "현재가", "전일비", "등락률", ...]
# title = "매물	매물특징	공급/전용면적	해당층/총층	방수/욕실수	월관리비	관리비 포함	융자금	기보증금/월세	방향	현관구조	난방(방식/연료)	입주가능일	총주차대수	매물번호	매물설명	중개사".split("\t")
# writer.writerow(title)


# 스크랩핑 반복
for index, item in enumerate(items):
	# 리스트 목록을 하나씩 클릭해서 beautifulSoup 으로 읽고 내용 스크랩핑 하기
	items[index].click()
	time.sleep(5)

	soup = BeautifulSoup(browser.page_source, "lxml") # 현재 페이지 스크랩 (browser.page_source)

	# 네이버 부동산 (매물정보)
	summary_table_rows = soup.find_all("table", attrs={"class":"info_table_wrap"})[0].find("tbody").find_all("tr")
	# print(data_rows) # 출력 확인

	# 매물 제목 csv 파일에 내보내기
	sales_title = soup.find("div", attrs={"class":"info_total_wrap"}).get_text()
	# print("매물 : ", sales_title) # 출력 확인
	writer.writerow(["매물정보"])
	writer.writerow([sales_title])
	writer.writerow("\n")

#  --- previous work start---
# 매물내용을 번호를 순서대로 찍어 출력하기
	# # 매물의 제목 출력
	# print()
	# print("==============================================")
	# sales_title = soup.find("h4", attrs={"class":"info_title"}).get_text(" ")
	# print("매물 : ", sales_title)

	# # for 문을 이용하여 tr 를 스캔하고 매물 내용 (th 과 td) 를 출력하기를 반복하기
	# for index, row in enumerate(table_rows):

	# 	# 매물의 table header
	# 	sales_header = row.find_all("th")[0].get_text().strip()
	# 	# 매물의 table info
	# 	sales_info = row.find_all("td")[0].get_text().strip()

	# 	print("{}.".format(index+1), sales_header, ":", sales_info)

	# 	# td 갯수 확인. 만약에 2개 이상일땐 2번째도 출력. 없다면 계속 진행
	# 	if len(row.find_all("td")) >= 2:
	# 		# BUG: index 를 increment 해도 for 루프가 다시 시작 되면서 if 안에 increment 가 지워짐

	# 		# 매물의 2번째 header, info 출력
	# 		sales_header = row.find_all("th")[1].get_text().strip()
	# 		sales_info = row.find_all("td")[1].get_text().strip()
			
	# 		print("{}.".format(index+1), sales_header, ":", sales_info)
#  --- previous work end---

# 매물 헤더, 내용 csv 파일로 내보내기
	for row in summary_table_rows:
		# 매물의 header 들을 리스트에 저장
		sales_headers = row.find_all("th")
		sales_headers_data = [sales_header.get_text().strip() for sales_header in sales_headers]
		writer.writerow(sales_headers_data)

		# 매물의 info 들을 리스트에 저장
		sales_infos = row.find_all("td")
		sales_infos_data =  [sales_info.get_text().strip() for sales_info in sales_infos]
		writer.writerow(sales_infos_data)

		# 내용 출력 후 줄 바꿈
		writer.writerow("\n")
	# 매물 테이블정보 출력 후 줄 바꿈 
	writer.writerow("\n")

	# 네이버 부동산 (중개보수 및 세금 정보)
	dues_table_rows = soup.find_all("table", attrs={"class":"info_table_wrap"})[1].find("tbody").find_all("tr")

	for row in dues_table_rows:
		# 매물의 header 들을 리스트에 저장
		sales_headers = row.find_all("th")
		sales_headers_data = [sales_header.get_text().strip() for sales_header in sales_headers]
		writer.writerow(sales_headers_data)

		# 매물의 info 들을 리스트에 저장
		sales_infos = row.find_all("td")
		sales_infos_data =  [sales_info.get_text().strip() for sales_info in sales_infos]
		writer.writerow(sales_infos_data)

		# 내용 출력 후 줄 바꿈
		writer.writerow("\n")
	# 매물 테이블정보 출력 후 줄 바꿈 
	writer.writerow("\n")

	# 네이버 부동산 (관리비)
	manage_table_rows = soup.find("table", attrs={"class":"manage_table_wrap"}).find("tbody").find_all("tr")

	for row in manage_table_rows:
		# 매물의 header 들을 리스트에 저장
		sales_headers = row.find_all("th")
		sales_headers_data = [sales_header.get_text().strip() for sales_header in sales_headers]
		writer.writerow(sales_headers_data)

		# 매물의 info 들을 리스트에 저장
		sales_infos = row.find_all("td")
		sales_infos_data =  [sales_info.get_text().strip() for sales_info in sales_infos]
		writer.writerow(sales_infos_data)

		# 내용 출력 후 줄 바꿈
		writer.writerow("\n")
	# 한 매물 출력 완료 후 줄 바꿈 
	writer.writerow(["============================================================"])
	writer.writerow("\n")

# 스크랩핑 완료 알림
print("스크랩핑 완료")
# time.sleep(3)
browser.quit()