import os, json, random, requests, markdown, urllib.parse, feedparser, tweepy, time, re
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def get_env(key):
    val = os.environ.get(key, "")
    if not val or "***" in val: return ""
    return val.strip()

# [설정]
AMAZON_TAG = "empireanalyst-20"
BYBIT_LINK = "https://www.bybit.com/invite?ref=DOVWK5A"
BLOG_BASE_URL = "https://ramuh18.github.io/zombie-bot/"
EMPIRE_URL = "https://empire-analyst.digital"

GEMINI_API_KEY = get_env("GEMINI_API_KEY")
DEVTO_TOKEN = get_env("DEVTO_TOKEN")
X_API_KEY = get_env("X_API_KEY")
X_API_SECRET = get_env("X_API_SECRET")
X_ACCESS_TOKEN = get_env("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = get_env("X_ACCESS_TOKEN_SECRET")

# [1. 뉴스 주제 가져오기]
def get_hot_topic():
    topics = [
        "Bitcoin Institutional Adoption 2026",
        "Gold vs. US Dollar Outlook",
        "AI Tech Sector Valuation Risks",
        "Global Supply Chain & Inflation",
        "Ethereum ETF Market Impact"
    ]
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        if feed.entries: return feed.entries[0].title
    except: pass
    return random.choice(topics)

# [2. 글 세척기 (AI가 뱉은 껍질 벗기기)]
def clean_content(text):
    text = text.strip()
    # JSON 파싱 시도
    if text.startswith("{") or "reasoning_content" in text:
        try:
            data = json.loads(text)
            if 'content' in data: return data['content']
            if 'choices' in data: return data['choices'][0]['message']['content']
        except:
            # 파싱 실패하면 정규식으로 'content' 내부만 추출
            match = re.search(r'"content":\s*"(.*?)"', text, re.DOTALL)
            if match: return match.group(1).replace('\\n', '\n').replace('\\"', '"')
            
    # 마크다운 제목(#) 앞의 잡설 제거
    if '#' in text:
        text = text[text.find('#'):]
        
    return text

# [3. 글쓰기 엔진 (재시도 기능 탑재)]
def generate_article_body(topic):
    log(f"🧠 주제: {topic}")
    prompt = f"""
    Act as a Senior Financial Analyst. Write a structured blog post about '{topic}'.
    - Structure: Introduction, Key Drivers, Market Outlook, Conclusion.
    - Style: Professional, Insightful, Concise.
    - Format: Pure Markdown only. Use ## for headings.
    - NO JSON. NO conversational filler.
    """
    
    # 최대 3번 시도 (글 망치면 다시 시킴)
    for attempt in range(3):
        try:
            log(f"✍️ 글쓰기 시도 {attempt+1}/3...")
            
            # 1순위: Gemini
            if GEMINI_API_KEY:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
                resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
                if resp.status_code == 200:
                    text = resp.json()['candidates'][0]['content']['parts'][0]['text']
                    clean = clean_content(text)
                    if len(clean) > 200: return clean # 성공!

            # 2순위: 무료 AI
            url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
            resp = requests.get(url, timeout=60)
            clean = clean_content(resp.text)
            
            # 검증: 외계어(JSON)나 너무 짧은 글은 실패 처리
            if "reasoning_content" in clean or len(clean) < 200:
                log("⚠️ 글 품질 미달. 재시도합니다.")
                continue # 다음 시도로
                
            return clean # 성공!
            
        except Exception as e:
            log(f"❌ 에러 발생: {e}")
            time.sleep(2)

    # 3번 다 실패했을 때만 나가는 최후의 원고
    log("🚨 모든 AI 시도 실패. 비상 원고 사용.")
    return f"""
    ## Market Update: {topic}
    
    **Executive Summary**
    The market is showing increased volatility surrounding {topic}. Institutional investors are repositioning portfolios to manage risk.
    
    **Key Insights**
    * **Trend Analysis:** Current price action suggests a consolidation phase.
    * **Risk Factors:** Macroeconomic indicators remain mixed.
    
    **Outlook**
    We recommend a cautious approach, focusing on high-quality assets like Gold and Bitcoin.
    """

# [4. 메인 실행 (건축가 역할)]
def main():
    log("🏁 Empire Analyst (Perfect Layout) 가동")
    topic = get_hot_topic()
    
    # 1. AI에게 글만 받아옴 (디자인 X)
    raw_md = generate_article_body(topic)
    html_content = markdown.markdown(raw_md)
    
    # 2. 파이썬이 디자인을 입힘 (여기서 바이비트 강제 삽입)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(topic + ' chart 8k')}"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # ★ 바이비트/아마존 섹션 (파이썬이 직접 그림)
    ads_section = f"""
    <div style="margin-top: 40px; padding: 30px; background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 12px; text-align: center;">
        <h3 style="margin-top: 0; color: #2d3436;">💰 Exclusive Trader Offers</h3>
        <p style="color: #636e72; margin-bottom: 20px;">Maximize your portfolio with our partners.</p>
        <div style="display: flex; flex-direction: column; gap: 12px;">
            <a href="{BYBIT_LINK}" target="_blank" style="display: block; padding: 16px; background: #121212; color: #f7a600; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 1.1em;">
                🎁 Claim $30,000 Bybit Bonus
            </a>
            <a href="https://www.amazon.com/s?k=ledger+nano&tag={AMAZON_TAG}" target="_blank" style="display: block; padding: 16px; background: #ff9900; color: white; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 1.1em;">
                🛡️ Secure Crypto with Ledger (Amazon)
            </a>
        </div>
    </div>
    """

    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{topic}</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
            img {{ width: 100%; height: auto; border-radius: 12px; margin: 20px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
            h1 {{ font-size: 2.5rem; margin-bottom: 10px; border-bottom: 2px solid #f1f1f1; padding-bottom: 15px; }}
            h2 {{ color: #2c3e50; margin-top: 30px; }}
            .badge {{ display: inline-block; background: #e74c3c; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: bold; margin-bottom: 10px; }}
            .footer {{ margin-top: 60px; padding-top: 20px; border-top: 1px solid #eee; text-align: center; color: #888; font-size: 0.9rem; }}
            a {{ color: #0070f3; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <span class="badge">LIVE UPDATE: {current_time}</span>
        <h1>{topic}</h1>
        <img src="{img_url}" alt="Market Chart">
        
        <div class="content">
            {html_content}
        </div>
        
        {ads_section}
        
        <div class="footer">
            <p>Analysis provided by <strong>Empire Analyst Systems</strong></p>
            <p><a href="{EMPIRE_URL}">Visit Official Headquarters →</a></p>
        </div>
    </body>
    </html>
    """

    # 저장
    try:
        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
        log("✅ index.html 저장 완료")
    except Exception as e: log(f"❌ 저장 실패: {e}")

    # 배포 (Dev.to / X)
    if DEVTO_TOKEN:
        try: requests.post("https://dev.to/api/articles", headers={"api-key": DEVTO_TOKEN}, json={"article": {"title": topic, "published": True, "body_markdown": raw_md, "canonical_url": BLOG_BASE_URL}}, timeout=10)
        except: pass
    if X_API_KEY:
        try:
            client = tweepy.Client(X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET)
            client.create_tweet(text=f"⚡ Market Alert: {topic}\n\nFull Report: {BLOG_BASE_URL}")
        except: pass

if __name__ == "__main__":
    main()
