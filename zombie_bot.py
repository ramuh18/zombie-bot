import os, json, random, requests, markdown, urllib.parse, feedparser, tweepy, time, re
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [설정 로드]
AMAZON_TAG = "empireanalyst-20"
BYBIT_LINK = "https://www.bybit.com/invite?ref=DOVWK5A"
BLOG_BASE_URL = "https://ramuh18.github.io/zombie-bot/" 
EMPIRE_URL = "https://empire-analyst.digital"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DEVTO_TOKEN = os.environ.get("DEVTO_TOKEN")
X_API_KEY = os.environ.get("X_API_KEY")
X_API_SECRET = os.environ.get("X_API_SECRET")
X_ACCESS_TOKEN = os.environ.get("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.environ.get("X_ACCESS_TOKEN_SECRET")

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
    """AI의 '속마음(JSON/코드)'을 완벽히 제거하고 본문만 추출"""
    raw_text = raw_text.strip()
    # JSON 형태면 내용물만 추출
    if raw_text.startswith('{'):
        try:
            data = json.loads(raw_text)
            if 'content' in data: return data['content']
            if 'choices' in data: return data['choices'][0]['message']['content']
        except:
            # 파싱 실패 시 정규식으로 "content":"..." 사이 추출
            match = re.search(r'"content":\s*"(.*?)"', raw_text, re.DOTALL)
            if match:
                clean = match.group(1).replace('\\n', '\n').replace('\\"', '"')
                return clean
    
    # 마크다운 헤더(#)가 있는 부분부터 진짜 글로 간주
    if '#' in raw_text:
        return raw_text[raw_text.find('#'):]
    return raw_text

# [3. 콘텐츠 엔진]
def generate_content(topic):
    keyword = "Gold" if "Gold" in topic else "AI Tech"
    log(f"🧠 {keyword} 중심의 심층 리포트 작성 중...")
    
    # 블룸버그 기사 스타일의 페르소나 주입
    prompt = f"""
    Act as a Senior Analyst at Bloomberg. Write a 1000-word deep-dive report.
    Topic: {topic}
    Requirements:
    1. Use professional terminology (P/E Ratio, CAGR, Institutional Appetite).
    2. Focus on the 2026 outlook: AI Tech Bubble ($300M+ valuations) vs Gold ($2,210/oz).
    3. Sections: Macro Equilibrium, Sector-Specific Risks, Investor Sentiment, Strategic Bottom Line.
    4. Format: Markdown. Do not include any JSON or system messages.
    """
    
    # 1차: Gemini
    if GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
            if resp.status_code == 200:
                return clean_text(resp.json()['candidates'][0]['content']['parts'][0]['text'])
        except: pass

    # 2차: 무료 AI (Pollinations)
    try:
        url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
        resp = requests.get(url, timeout=60)
        if resp.status_code == 200:
            return clean_text(resp.text)
    except: pass

    return f"# Market Alert: {topic}\n\nThe tug-of-war between AI innovation and Gold's safety continues in 2026."

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
        
        # 디자인 강화 레이아웃
        html_body = markdown.markdown(raw_md)
        full_html = f"""
        <!DOCTYPE html>
        <html><head>
            <title>Empire Analyst | {topic}</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: 'Inter', -apple-system, sans-serif; max-width: 800px; margin: auto; padding: 40px 20px; line-height: 1.8; color: #2d3436; background: #fff; }}
                .tag {{ background: #fab1a0; color: #d63031; padding: 4px 12px; border-radius: 50px; font-size: 0.8em; font-weight: bold; text-transform: uppercase; }}
                h1 {{ font-size: 2.8em; line-height: 1.2; margin: 20px 0; letter-spacing: -1px; }}
                img {{ width: 100%; border-radius: 16px; margin: 30px 0; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }}
                .promo-card {{ background: #f1f2f6; border-radius: 16px; padding: 30px; margin: 50px 0; border: 1px solid #dfe6e9; }}
                .btn {{ display: block; padding: 18px; text-align: center; border-radius: 10px; font-weight: bold; text-decoration: none; margin: 15px 0; transition: 0.3s; }}
                .btn-amz {{ background: #ff9900; color: white; }}
                .btn-bybit {{ background: #1a1a1a; color: #f9aa33; }}
                .footer-card {{ background: #000; color: white; padding: 50px 30px; border-radius: 20px; text-align: center; margin-top: 80px; }}
                .footer-card a {{ color: #00a8ff; font-weight: bold; text-decoration: none; border: 1px solid #00a8ff; padding: 10px 25px; border-radius: 30px; }}
            </style>
        </head>
        <body>
            <span class="tag">Exclusive Report • {timestamp}</span>
            <h1>{topic}</h1>
            <img src="{img_url}">
            <div class="content">{html_body}</div>
            
            <div class="promo-card">
                <h3 style="margin-top:0;">🛡️ Strategic Asset: {keyword}</h3>
                <a href="{amz_link}" class="btn btn-amz">🛒 Check {keyword} Market Prices</a>
                <a href="{BYBIT_LINK}" class="btn btn-bybit">🎁 Claim $30,000 Trading Bonus</a>
            </div>

            <div class="footer-card">
                <div style="font-size:3em;">🏛️</div>
                <h2 style="color:white;margin:10px 0;">Empire Analyst</h2>
                <p style="color:#636e72;margin-bottom:30px;">Intelligence for the Sovereign Investor</p>
                <a href="{EMPIRE_URL}">VISIT HEADQUARTERS →</a>
                <p style="font-size:0.7em; color:#2d3436; margin-top:40px;">© 2026 Empire Analyst. All Rights Reserved.</p>
            </div>
        </body></html>
        """
        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
        log("✅ 리포트 생성 완료")
    except Exception as e: log(f"❌ 실패: {e}")

    # Dev.to & X 업로드
    if DEVTO_TOKEN:
        requests.post("https://dev.to/api/articles", headers={"api-key": DEVTO_TOKEN}, json={"article": {"title": topic, "published": True, "body_markdown": raw_md, "canonical_url": BLOG_BASE_URL}})
    if X_API_KEY:
        try:
            client = tweepy.Client(X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET)
            client.create_tweet(text=f"⚡ {topic}\n\nRead the full 2026 Bloomberg-style analysis 👇\n{BLOG_BASE_URL}\n\n#Finance #AI #Gold")
        except: pass

if __name__ == "__main__":
    main()
