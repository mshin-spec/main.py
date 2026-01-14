import feedparser
import requests
from datetime import datetime
import re

# [필수 설정]
TOKEN = "8070079193:AAEKHha5VfHNli7YT29nSSqjV4dILYRGdGE"
CHAT_ID = "948672091" # 유령 문자 제거됨
KEYWORDS = ["가축분뇨처리", "준공영제", "사모펀드", "부동산"]

def send_telegram_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID, 
        'text': text, 
        'parse_mode': 'Markdown',
        'disable_web_page_preview': True
    }
    response = requests.post(url, data=payload)
    # 전송 실패 시 로그 출력 (GitHub Actions 로그에서 확인 가능)
    if response.status_code != 200:
        print(f"Error: {response.text}")

def scrap_news():
    today = datetime.now().strftime('%Y-%m-%d')
    final_report = f"📅 *{today} 뉴스 큐레이션*\n\n"
    sent_links = set()
    
    for keyword in KEYWORDS:
        rss_url = f"https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"
        feed = feedparser.parse(rss_url)
        
        keyword_section = f"🔍 *{keyword}*\n"
        has_new_content = False
        
        count = 0
        for entry in feed.entries:
            if count >= 3: break
            if entry.link in sent_links: continue
            
            # 마크다운 충돌 방지: 제목 내 [ ] 제거
            clean_title = entry.title.split(" - ")[0]
            clean_title = clean_title.replace("[", "(").replace("]", ")")
            
            keyword_section += f"• [{clean_title}]({entry.link})\n"
            
            sent_links.add(entry.link)
            count += 1
            has_new_content = True
        
        if has_new_content:
            final_report += keyword_section + "\n"

    if sent_links:
        send_telegram_msg(final_report)
    else:
        send_telegram_msg(f"📅 {today}: 새로운 뉴스가 없습니다.")

if __name__ == "__main__":
    scrap_news()