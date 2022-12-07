# 웹 스크래핑 보드
# 텔레그램 push
# django로 DB 저장하기
import requests
from bs4 import BeautifulSoup
import telegram
# import telegram_info as ti django-extension 설치 하기 전
# from . import telegram_info as ti django-extension 설치 하기 후
from hotdeal.models import Deal
import env_info as ti # 루트 변경
from datetime import datetime, timedelta

# db 테이블 데이터 유지가간 설정 변수
during_date = 3

# DB 테이블 저장을 위한 추천 갯수 지정
up_cnt_limit = 3

TLGM_BOT_API = ti.TLGM_BOT_API
tlgm_bot = telegram.Bot(TLGM_BOT_API)
# https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu  <크롤링할 사이트 [뽐뿌]>
url = 'https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu'
res = requests.get(url)

# print(res) <Response [200]>
# print(res.text)

soup = BeautifulSoup(res.text ,"html.parser") # text로 받은 결과를 html로 파싱하라.
# print(soup) # 출력은 똑같지만 Bs객체로 하나하나씩 요소 지정 가능.
    # print(items)

def run():
    # DB 테이블에 3일치만 유지함
    # row, _ = Deal.objects.filter(cdate__lte=datetime.now() - timedelta(day=3)).delete()
    row, _ = Deal.objects.filter(cdate__lte=datetime.now() - timedelta(minutes=during_date)).delete()
    print( row, "deals deleted")
    items = soup.select("tr.list1,tr.list0")
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
            reply_count = item.select("td span.list_comment2 span")[0].text.strip()
            up_count = item.select("td.eng.list_vspace")[-2].text.strip()
            up_count = up_count.split("-")[0]
            up_count = int(up_count)
            if up_count >= up_cnt_limit:
                db_link_cnt = Deal.objects.filter(link__iexact=link).count()
                
                # 텔레그램 봇으로 push
                caht_id = ti.caht_id # 채팅 채널 id
                message = f"{title} {img_url}"
                #tlgm_bot.sendMessage(chat_di, 전송_message)
                tlgm_bot.sendMessage(caht_id, message)
                
                # print(up_count)
                # hotdeal 앱의 deal클래스를 통해 DB 테이블에 데이터 저장
                if(db_link_cnt==0):
                    # 중복제거를 위해서 filter안 사용!
                    Deal(img_url=img_url, title=title, link=link,
                        reply_count=reply_count, up_count=up_count).save()
                # 터미널 프린트
                # print(img_url, title, link, reply_count, up_count)
                
        except Exception as e :
            continue

