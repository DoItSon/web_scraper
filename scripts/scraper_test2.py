import requests
from bs4 import BeautifulSoup
import telegram

res = requests.get("https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu")

asoup = BeautifulSoup(res.text, "html.parser")
TLGM_BOT_TOKEN = "5572644037:AAF2-dJcGWqmLhg1U6JN41M8PUh2D0yswMs"
tlgm_bot = telegram.Bot(token=TLGM_BOT