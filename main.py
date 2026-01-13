import feedparser
import requests

# [필수 설정]
TOKEN = "8070079193:AAEKHha5VfHNli7YT29nSSqjV4dILYRGdGE"
CHAT_ID = "948672091" 

# [추가 작업] 원하는 키워드를 리스트 형태로 나열하세요.
KEYWORDS = ["가축분뇨처리", "사모펀드", "준공영제"]

def send_telegram_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'Markdown'}
    requests.post(url, data=payload)

def scrap_news():
    sent_links = set() # 중복 전송 방지를 위한 저장소
    
    for keyword in KEYWORDS:
        rss_url = f"https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"
        feed = feedparser.parse(rss_url)
        
        # 키워드별 구분선 전송
        # send_telegram_msg(f"🔍 **키워드: {keyword}**")
        
        count = 0
        for entry in feed.entries:
            if count >= 2: break # 키워드당 최신 뉴스 2개로 제한 (도배 방지)
            
            # 다른 키워드에서 이미 보낸 링크라면 건너뜀 (중복 제거)
            if entry.link in sent_links:
                continue
                
            msg = f"📌 [{keyword}] {entry.title}\n🔗 {entry.link}"
            send_telegram_msg(msg)
            
            sent_links.add(entry.link)
            count += 1

if __name__ == "__main__":
    scrap_news()