import os, json, random, requests, markdown, urllib.parse, feedparser, tweepy, time, re
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def get_env(key):
    val = os.environ.get(key, "")
    if not val or "***" in val: return ""
    return val.strip()

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
        # 매번 조금씩 다른 주제를 가져오도록 유도
        topics = ["Global Market Volatility", "Crypto vs Gold 2026", "AI Tech Bubble Risks", "Fed Interest Rate Strategy"]
        return random.choice(topics)
    except: 
        return "Global Market Outlook"

# [2. 콘텐츠 엔진: AI가 실수하면 바로 수동 모드 발동]
def generate_content(topic):
    log(f"🧠 '{topic}' 기사 작성 시도...")
    
    # 1. Gemini 시도 (가장 안전)
    if GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            prompt = f"Write a professional financial report about {topic}. Markdown only. No JSON."
            resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
            if resp.status_code == 200:
                text = resp.json()['candidates'][0]['content']['parts'][0]['text']
                if "{" not in text and "reasoning_content" not in text:
                    return text # 깨끗하면 반환
        except: pass

    # 2. 무료 AI 시도
    try:
        prompt = f"Write a financial news article about {topic}. Do not output JSON code."
        url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
        resp = requests.get(url, timeout=60)
        text = resp.text.strip()

        # ★ [핵심] 외계어 감지 시 즉시 'None' 반환 -> 수동 모드로 직행
        # 사용자님이 보여주신 'role', 'reasoning_content', '{' 등이 보이면 가차 없이 버림
        if "reasoning_content" in text or '{"role":' in text or text.startswith("{"):
            log("🚨 외계어(JSON) 감지! -> 수동 모드로 전환합니다.")
            return None 
            
        return text
    except: pass
    
    return None # 실패 시 None

# [3. 수동 모드 원고 (절대 안 깨지는 HTML)]
def get_backup_html(topic):
    return f"""
    <div style="padding: 20px; background-color: #fff3cd; color: #856404; border-radius: 8px; margin-bottom: 30px;">
        <strong>⚠️ Analyst Note:</strong> Automated feed is calibrating. Displaying manual executive summary.
    </div>

    <h3>1. Market Overview: {topic}</h3>
    <p>The financial markets are currently navigating a period of heightened volatility. Institutional capital is rotating from high-growth tech stocks into defensive assets such as <strong>Gold</strong> and <strong>Government Bonds</strong>.</p>
    
    <h3>2. Key Drivers</h3>
    <ul>
        <li><strong>Institutional Volume:</strong> Significant accumulation is observed in safe-haven assets.</li>
        <li><strong>Technical Levels:</strong> Major indices are testing critical support zones.</li>
        <li><strong>Macro Sentiment:</strong> Inflation concerns are resurfacing, prompting a "risk-off" approach from hedge funds.</li>
    </ul>

    <h3>3. Strategic Outlook</h3>
    <p>"In the current environment, cash preservation and selective entry into commodities offer the best risk-adjusted returns," notes the <strong>Empire Analyst</strong> strategy team.</p>
    """

# [4. 메인 실행]
def main():
    log("🏁 Zombie Bot (Fail-Safe Ver) 가동")
    topic = get_hot_topic()
    
    # AI 기사 생성 시도
    raw_md = generate_content(topic)
    
    # AI가 성공했으면 마크다운 변환, 실패했으면 수동 HTML 사용
    if raw_md:
        log("✅ AI 기사 생성 성공")
        html_body = markdown.markdown(raw_md)
    else:
        log("🛡️ AI 실패/외계어 감지 -> 수동 원고 투입")
        html_body = get_backup_html(topic)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    keyword = "Finance"

    try:
        img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(topic + ' chart 8k')}"
        amz_link = f"https://www.amazon.com/s?k=gold&tag={AMAZON_TAG}"
        
        full_html = f"""
        <!DOCTYPE html>
        <html><head><title>Empire Analyst</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: 'Helvetica', sans-serif; max-width: 800px; margin: auto; padding: 40px 20px; line-height: 1.8; color: #333; }}
            img {{ width: 100%; border-radius: 12px; margin: 30px 0; }}
            h1 {{ font-size: 2.2em; border-bottom: 2px solid #eee; padding-bottom: 15px; letter-spacing: -1px; }}
            .time-tag {{ background: #000; color: #fff; padding: 5px 10px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }}
            .footer-card {{ background: #111; color: white; padding: 60px 20px; border-radius: 20px; text-align: center; margin-top: 80px; }}
            .btn {{ background: #fff; color: #000; padding: 12px 25px; text-decoration: none; border-radius: 30px; font-weight: bold; }}
        </style></head>
        <body>
            <span class="time-tag">UPDATED: {current_time}</span>
            <h1 style="margin-top:20px;">{topic}</h1>
            <img src="{img_url}">
            
            {html_body}
            
            <div style="background:#f9f9f9; padding:25px; text-align:center; border-radius:12px; margin-top:40px; border:1px solid #eee;">
                 <h3 style="margin-top:0;">🛡️ Empire Selection</h3>
                 <p>Hedge against market risks.</p>
                 <a href="{amz_link}" style="background:#ff9900; color:white; padding:10px 20px; text-decoration:none; border-radius:5px; font-weight:bold;">Check Gold Prices</a>
            </div>

            <div class="footer-card">
                <h2>Empire Analyst</h2>
                <p style="color:#888;">Automated Financial Intelligence</p>
                <a href="{EMPIRE_URL}" class="btn">VISIT HEADQUARTERS →</a>
            </div>
        </body></html>
        """
        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
        log("✅ index.html 저장 완료")
    except Exception as e: log(f"❌ 저장 실패: {e}")

    # 업로드 (에러 무시)
    if DEVTO_TOKEN:
        try: requests.post("https://dev.to/api/articles", headers={"api-key": DEVTO_TOKEN}, json={"article": {"title": topic, "published": True, "body_markdown": raw_md if raw_md else "Market Update", "canonical_url": BLOG_BASE_URL}}, timeout=10)
        except: pass
    if X_API_KEY:
        try:
            client = tweepy.Client(X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET)
            client.create_tweet(text=f"⚡ {topic}\n\nUpdate ({current_time}): {BLOG_BASE_URL}")
        except: pass

if __name__ == "__main__":
    main()
