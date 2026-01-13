import feedparser
import requests

def send_telegram_msg(text):
    url = f"https://api.telegram.org/bot{8070079193:AAEKHha5VfHNli7YT29nSSqjV4dILYRGdGE}/sendMessage?chat_id={948672091}&text={text}"
    requests.get(url)

def scrap_news():
    rss_url = f"https://news.google.com/rss/search?q={가축분뇨}&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)
    
    for entry in feed.entries[:3]: # 최신 3개만
        msg = f"📰 뉴스: {entry.title}\n🔗 링크: {entry.link}"
        send_telegram_msg(msg)

if __name__ == "__main__":
    scrap_news()