import feedparser
import requests

# [필수 설정] 본인의 정보를 입력하세요
TOKEN = "8070079193:AAEKHha5VfHNli7YT29nSSqjV4dILYRGdGE"
CHAT_ID = "948672091" 
KEYWORD = "가축분뇨" # 검색하고 싶은 키워드

def send_telegram_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': text}
    requests.post(url, data=payload)

def scrap_news():
    # 중괄호 안에 변수명 KEYWORD를 넣어 올바르게 작동하게 함
    rss_url = f"https://news.google.com/rss/search?q={KEYWORD}&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)
    
    if not feed.entries:
        send_telegram_msg(f"'{KEYWORD}'에 대한 새로운 뉴스가 없습니다.")
        return

    for entry in feed.entries[:3]: # 최신 뉴스 3개
        msg = f"📰 뉴스: {entry.title}\n🔗 링크: {entry.link}"
        send_telegram_msg(msg)

if __name__ == "__main__":
    scrap_news()