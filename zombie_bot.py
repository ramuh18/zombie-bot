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

# [1. 주제 선정]
def get_hot_topic():
    topics = [
        "Bitcoin vs Gold: Safe Haven Analysis 2026",
        "AI Bubble Risks: Tech Sector Outlook",
        "Global Inflation & Interest Rates 2026",
        "Ethereum ETF: Market Impact Report"
    ]
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        if feed.entries: return feed.entries[0].title
    except: pass
    return random.choice(topics)

# [2. 글 세척기 (무료 AI 광고 박멸)]
def clean_content(text):
    text = text.strip()
    
    # JSON 제거
    if text.startswith("{") or "reasoning_content" in text:
        try:
            data = json.loads(text)
            if 'content' in data: text = data['content']
            elif 'choices' in data: text = data['choices'][0]['message']['content']
        except:
            match = re.search(r'"content":\s*"(.*?)"', text, re.DOTALL)
            if match: text = match.group(1).replace('\\n', '\n').replace('\\"', '"')

    # 광고 문구 제거
    patterns = [r"Powered by Pollinations\.AI.*", r"Support our mission.*", r"🌸 Ad 🌸.*", r"Running on free AI.*"]
    for p in patterns:
        text = re.sub(p, "", text, flags=re.IGNORECASE)

    # 마크다운 헤더 정리
    if '#' in text: text = text[text.find('#'):]

    return text.strip()

# [3. 글쓰기 엔진]
def generate_article_body(topic):
    log(f"🧠 주제: {topic}")
    prompt = f"""
    Act as a Senior Financial Analyst. Write a deep-dive report on '{topic}'.
    Structure: Executive Summary, Key Drivers, Outlook. 
    Format: Markdown. NO JSON. NO ADS.
    """
    
    for attempt in range(3):
        try:
            if GEMINI_API_KEY:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
                resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
                if resp.status_code == 200:
                    text = resp.json()['candidates'][0]['content']['parts'][0]['text']
                    clean = clean_content(text)
                    if len(clean) > 200: return clean

            url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
            resp = requests.get(url, timeout=60)
            clean = clean_content(resp.text)
            if len(clean) > 200: return clean
        except: time.sleep(2)

    return f"## Analysis Update: {topic}\n\nMarket data is processing. Please check back shortly."

# [4. 메인 실행 (블랙 헤더 적용)]
def main():
    log("🏁 Empire Analyst (Black Header Ver) 가동")
    topic = get_hot_topic()
    raw_md = generate_article_body(topic)
    html_content = markdown.markdown(raw_md)
    
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(topic + ' chart 8k')}"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # ★ 디자인 변경: 헤더를 검은색으로 변경하여 업데이트 확인 용이하게 함
    header_section = f"""
    <div style="background: #111; color: white; padding: 40px 20px; text-align: center; margin-bottom: 40px; border-radius: 0 0 20px 20px;">
        <div style="font-size: 0.9rem; font-weight: bold; color: #f1c40f; letter-spacing: 2px; margin-bottom: 10px;">PREMIUM INTELLIGENCE</div>
        <div style="font-family: serif; font-size: 2.8rem; font-weight: 900; margin-bottom: 5px;">EMPIRE ANALYST</div>
        <div style="font-size: 0.8rem; color: #888;">EST. 2026 • QUANTITATIVE INSIGHTS</div>
    </div>
    """

    ads_section = f"""
    <div style="margin: 50px 0; padding: 30px; background: #f8f9fa; border: 1px solid #ddd; border-radius: 12px; text-align: center;">
        <h3 style="margin-top: 0; color: #2d3436;">⚡ Strategic Portfolio</h3>
        <div style="display: flex; flex-direction: column; gap: 15px; max-width: 400px; margin: 20px auto 0;">
            <a href="{BYBIT_LINK}" style="background: #000; color: #f1c40f; padding: 15px; border-radius: 8px; text-decoration: none; font-weight: bold;">🎁 Claim $30,000 Bybit Bonus</a>
            <a href="https://www.amazon.com/s?k=gold&tag={AMAZON_TAG}" style="background: #ff9900; color: white; padding: 15px; border-radius: 8px; text-decoration: none; font-weight: bold;">🛡️ Check Gold Prices</a>
        </div>
    </div>
    """

    footer_section = f"""
    <div style="margin-top: 60px; padding: 40px 20px; background: #000; color: white; border-radius: 16px; text-align: center;">
        <h2 style="color: white; margin: 0 0 10px 0;">Empire Analyst HQ</h2>
        <a href="{EMPIRE_URL}" style="display: inline-block; background: white; color: black; padding: 10px 25px; border-radius: 30px; font-weight: bold; text-decoration: none; margin-top: 20px;">VISIT OFFICIAL SITE →</a>
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
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.8; color: #333; max-width: 800px; margin: 0 auto; background-color: #fff; padding-bottom: 50px; }}
            img {{ width: 100%; height: auto; border-radius: 8px; margin: 30px 0; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
            h1 {{ font-size: 2.2rem; margin-bottom: 10px; padding: 0 20px; }}
            .meta {{ font-size: 0.8rem; color: #999; margin-bottom: 20px; padding: 0 20px; text-transform: uppercase; }}
            .content {{ padding: 0 20px; }}
            a {{ color: #0070f3; text-decoration: none; }}
        </style>
    </head>
    <body>
        {header_section} <div class="meta">UPDATED: {current_time}</div>
        <h1>{topic}</h1>
        <img src="{img_url}" alt="Chart">
        
        <div class="content">
            {html_content}
        </div>
        
        {ads_section}
        {footer_section}
    </body>
    </html>
    """

    try:
        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
        log("✅ index.html 저장 완료")
    except Exception as e: log(f"❌ 저장 실패: {e}")

    if DEVTO_TOKEN:
        try: requests.post("https://dev.to/api/articles", headers={"api-key": DEVTO_TOKEN}, json={"article": {"title": topic, "published": True, "body_markdown": raw_md, "canonical_url": BLOG_BASE_URL}}, timeout=10)
        except: pass
    if X_API_KEY:
        try:
            client = tweepy.Client(X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET)
            client.create_tweet(text=f"⚡ Analysis: {topic}\n\nLink: {BLOG_BASE_URL}")
        except: pass

if __name__ == "__main__":
    main()
