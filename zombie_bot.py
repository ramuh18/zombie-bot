import os, json, random, requests, markdown, urllib.parse, feedparser, tweepy, time, re
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [설정 로드 - 비밀번호 세척 추가]
def get_env(key):
    val = os.environ.get(key, "")
    return val.strip() if val else "" # 공백 제거로 InvalidHeader 방지

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

# [1. 뉴스 엔진]
def get_hot_topic():
    try:
        log("📰 최신 금융 트렌드 분석 중...")
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        if feed.entries:
            return feed.entries[0].title
    except: pass
    return random.choice(["AI Tech Bubble & Gold Tug-of-War", "Bitcoin ETF Institutional Inflow", "Global Inflation & Hard Assets"])

# [2. 강력 세척 필터]
def clean_text(raw_text):
    raw_text = raw_text.strip()
    if raw_text.startswith('{'):
        try:
            data = json.loads(raw_text)
            if 'content' in data: return data['content']
            if 'choices' in data: return data['choices'][0]['message']['content']
        except:
            match = re.search(r'"content":\s*"(.*?)"', raw_text, re.DOTALL)
            if match: return match.group(1).replace('\\n', '\n').replace('\\"', '"')
    if '#' in raw_text: return raw_text[raw_text.find('#'):]
    return raw_text

# [3. 콘텐츠 엔진]
def generate_content(topic):
    keyword = "Gold" if "Gold" in topic else "AI Tech"
    log(f"🧠 {keyword} 중심의 심층 리포트 작성 중...")
    prompt = f"Act as a Senior Analyst at Bloomberg. Write a 1000-word deep-dive report about {topic}. Format: Markdown. No JSON."
    
    if GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
            if resp.status_code == 200:
                return clean_text(resp.json()['candidates'][0]['content']['parts'][0]['text'])
        except: pass

    try:
        url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
        resp = requests.get(url, timeout=60)
        if resp.status_code == 200: return clean_text(resp.text)
    except: pass
    return f"# Market Alert: {topic}\n\nThe tug-of-war continues."

# [4. 메인 실행]
def main():
    log("🏁 Empire Analyst Quantitative Bot 가동")
    topic = get_hot_topic()
    raw_md = generate_content(topic)
    keyword = "Gold" if "Gold" in topic else "AI"

    try:
        img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(topic + ' finance chart 8k')}"
        amz_link = f"https://www.amazon.com/s?k={keyword}&tag={AMAZON_TAG}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        html_body = markdown.markdown(raw_md)
        full_html = f"""
        <!DOCTYPE html>
        <html><head><title>Empire Analyst | {topic}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: sans-serif; max-width: 800px; margin: auto; padding: 40px 20px; line-height: 1.8; color: #2d3436; }}
            img {{ width: 100%; border-radius: 16px; margin: 30px 0; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }}
            .promo-card {{ background: #f1f2f6; border-radius: 16px; padding: 30px; margin: 50px 0; }}
            .btn {{ display: block; padding: 18px; text-align: center; border-radius: 10px; font-weight: bold; text-decoration: none; margin: 15px 0; }}
            .footer-card {{ background: #000; color: white; padding: 50px 30px; border-radius: 20px; text-align: center; }}
        </style></head>
        <body>
            <p>Exclusive Report • {timestamp}</p>
            <h1>{topic}</h1>
            <img src="{img_url}">
            {html_body}
            <div class="promo-card">
                <h3>🛡️ Strategic Asset: {keyword}</h3>
                <a href="{amz_link}" class="btn" style="background:#ff9900;color:white;">🛒 Check Prices</a>
                <a href="{BYBIT_LINK}" class="btn" style="background:#1a1a1a;color:#f9aa33;">🎁 Claim Bonus</a>
            </div>
            <div class="footer-card">
                <h2>Empire Analyst</h2>
                <a href="{EMPIRE_URL}" style="color:#00a8ff;">VISIT HEADQUARTERS →</a>
            </div>
        </body></html>
        """
        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
        log("✅ 리포트 생성 완료")
    except Exception as e: log(f"❌ HTML 생성 실패: {e}")

    # [수정됨] Dev.to 업로드 에러 방어
    if DEVTO_TOKEN and len(DEVTO_TOKEN) > 5:
        try:
            log("🚀 Dev.to 업로드 시도...")
            requests.post("https://dev.to/api/articles", 
                          headers={"api-key": DEVTO_TOKEN}, 
                          json={"article": {"title": topic, "published": True, "body_markdown": raw_md, "canonical_url": BLOG_BASE_URL}},
                          timeout=10)
        except Exception as e: log(f"⚠️ Dev.to 업로드 건너뜀: {e}")

    # [수정됨] 트위터 업로드 에러 방어
    if X_API_KEY and len(X_API_KEY) > 5:
        try:
            log("🐦 X(트위터) 업로드 시도...")
            client = tweepy.Client(X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET)
            client.create_tweet(text=f"⚡ {topic}\n\nRead more: {BLOG_BASE_URL}")
        except Exception as e: log(f"⚠️ X 업로드 건너뜀: {e}")

if __name__ == "__main__":
    main()
