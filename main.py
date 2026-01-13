import feedparser
import requests
from datetime import datetime

# [필수 설정]
TOKEN = "8070079193:AAEKHha5VfHNli7YT29nSSqjV4dILYRGdGE"
CHAT_ID = "948672091" 
KEYWORDS = ["가축분뇨처리", "준공영제", "사모펀드", "부동산"]

def send_telegram_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    # MarkdownV2를 사용하여 깔끔한 링크 스타일 적용
    payload = {
        'chat_id': CHAT_ID, 
        'text': text, 
        'parse_mode': 'Markdown',
        'disable_web_page_preview': True # 링크 미리보기 꺼서 공간 절약
    }
    requests.post(url, data=payload)

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
            if count >= 3: break # 키워드당 제목 3개 제한
            if entry.link in sent_links: continue
            
            # 제목에서 특수문자 처리 및 포맷팅
            clean_title = entry.title.split(" - ")[0] # 언론사명 제거하여 간결하게
            keyword_section += f"• [{clean_title}]({entry.link})\n"
            
            sent_links.add(entry.link)
            count += 1
            has_new_content = True
        
        if has_new_content:
            final_report += keyword_section + "\n"

    # 최종 취합된 메시지가 있을 경우에만 전송
    if sent_links:
        send_telegram_msg(final_report)
    else:
        send_telegram_msg(f"📅 {today}: 새로운 뉴스가 없습니다.")

if __name__ == "__main__":
    scrap_news()