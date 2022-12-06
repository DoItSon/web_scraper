# 웹 스크래핑 보드
import requests
from bs4 import BeautifulSoup
# https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu  <크롤링할 사이트 [뽐뿌]>

url = 'https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu'
res = requests.get(url)

# print(res) <Response [200]>
# print(res.text)

soup = BeautifulSoup(res.text ,"html.parser") # text로 받은 결과를 html로 파싱하라.
# print(soup) # 출력은 똑같지만 Bs객체로 하나하나씩 요소 지정 가능.
items = soup.select("tr.list1,tr.list0")
# print(items)

# img url, title, link, replay_count, up_count
for item in items:
    try:
        img_url = item.select("img.thumb_border")[0].get("src").strip() #[0]: 대괄호를 벗김 | get('src'):이미지 속성태그 | strip(): 공백제거
        title = item.select("a font.list_title")[0].text.strip() 
        # 중간에 비어있어서 index error 발생! (예외처리해줌) text는 문자만 뽑아냄!
        link = item.select("a font.list_title")[0].parent.get("href").strip()
        # parent = 클래스를 지정할 수 없을 때 사용한다.
        link = link.replace("/zboard/", "")
        link = link.lstrip('/')
        link = "https://www.ppomppu.co.kr/zboard/" + link
        # zboard가 있는 것도 있어서 replace를 없애고, 다시 / 붙이고 링크를 합침
        replay_count = item.select("td span.list_comment2 span")[0].text.strip()
        up_count = item.select("td.eng.list_vspace")[-2].text.strip()
        up_count = up_count.split("-")[0]
        up_count = int(up_count)
        # print(up_count)
    except Exception as e :
        continue
    