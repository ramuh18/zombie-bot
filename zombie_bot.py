import os, json, random, requests, markdown, urllib.parse, feedparser, tweepy, time, re
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [설정 로드: 공백 제거 및 안전장치]
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
        log("📰 실시간 금융 뉴스 수집 중...")
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        if feed.entries: return feed.entries[0].title
    except: pass
    return "Global Market Volatility & Crypto Trends"

# [2. 외계어 정밀 적출 수술대 (핵심)]
def clean_text(raw_text):
    """AI가 뱉은 잡동사니에서 '진짜 글'만 찾아내는 함수"""
    raw_text = raw_text.strip()
    
    # CASE 1: 완벽한 JSON 형태인 경우
    if raw_text.startswith('{'):
        try:
            data = json.loads(raw_text)
            # 'content'가 진짜 본문입니다.
            if 'content' in data and data['content']: return data['content']
            if 'choices' in data: return data['choices'][0]['message']['content']
        except:
            pass # JSON 파싱 실패하면 수동 분해 시도

    # CASE 2: JSON이 섞여 있거나 깨진 경우 (정규식으로 추출)
    # "content": "여기 있는 진짜 글" 을 찾아냅니다.
    match = re.search(r'"content"\s*:\s*"(.*?)"', raw_text, re.DOTALL)
    if match:
        extracted = match.group(1)
        # 깨진 문자(\n, \") 복구
        return extracted.replace('\\n', '\n').replace('\\"', '"').strip()

    # CASE 3: 마크다운 제목(#)으로 시작하는 부분이 있다면 거기부터가 본문
    if '#' in raw_text:
        return raw_text[raw_text.find('#'):]

    # CASE 4: 아무것도 해당 안 되면 원본 반환 (이미 깨끗한 경우)
    return raw_text

# [3. 콘텐츠 엔진]
def generate_content(topic):
    log(f"🧠 '{topic}' 주제로 기사 작성 시도...")
    prompt = f"Act as a Wall Street Analyst. Write a professional financial report about {topic}. Markdown format. No JSON wrapper."
    
    # 1차: Gemini (가장 성능 좋음)
    if GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
            if resp.status_code == 200:
                text = resp.json()['candidates'][0]['content']['parts'][0]['text']
                return clean_text(text)
        except: pass

    # 2차: 무료 AI (Pollinations) - 여기가 문제의 구간
    try:
        url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
        resp = requests.get(url, timeout=60)
        if resp.status_code == 200:
            # ★ 여기서 바로 포기하지 않고 'clean_text'로 수술 들어갑니다.
            return clean_text(resp.text)
    except: pass
    
    # 정 안되면 짧은 요약이라도 생성
    return f"# Market Report: {topic}\n\nAnalysis is currently updating. Please check back later."

# [4. 메인 실행 및 배포]
def main():
    log("🏁 Empire Analyst Bot (Pro Version) 가동")
    topic = get_hot_topic()
    
    # 1. 글 쓰기 (이제 매번 바뀝니다)
    raw_md = generate_content(topic)
    
    # 2. 혹시라도 글이 너무 짧거나(오류), 여전히 외계어면 비상용 제목만 붙임
    if not raw_md or len(raw_md) < 50:
        raw_md = f"# {topic}\n\nMarket data is being processed. Institutional flows suggest volatility."

    keyword = "Finance"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 3. GitHub Pages (HTML) 생성
    try:
        img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(topic + ' luxury finance chart 8k')}"
        amz_link = f"https://www.amazon.com/s?k=investment&tag={AMAZON_TAG}"
        
        html_body = markdown.markdown(raw_md)
        full_html = f"""
        <!DOCTYPE html>
        <html><head><title>Empire Analyst</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: 'Helvetica', sans-serif; max-width: 800px; margin: auto; padding: 40px 20px; line-height: 1.8; color: #333; }}
            img {{ width: 100%; border-radius: 12px; margin: 30px 0; box-shadow: 0 10px 20px rgba(0,0,0,0.1); }}
            h1 {{ font-size: 2.2em; border-bottom: 2px solid #eee; padding-bottom: 15px; letter-spacing: -1px; }}
            .promo {{ background: #f8f9fa; padding: 25px; border-radius: 12px; border: 1px solid #eee; margin-top: 40px; text-align: center; }}
            .footer-card {{ background: #111; color: white; padding: 60px 20px; border-radius: 20px; text-align: center; margin-top: 80px; }}
            .btn {{ background: #fff; color: #000; padding: 12px 25px; text-decoration: none; border-radius: 30px; font-weight: bold; transition: 0.3s; display: inline-block; }}
            .btn:hover {{ background: #eee; transform: translateY(-2px); }}
            a {{ color: #0070f3; text-decoration: none; }}
        </style></head>
        <body>
            <span style="color:#d63031; font-weight:bold; font-size:0.85em;">LIVE INTELLIGENCE • {timestamp}</span>
            <h1>{topic}</h1>
            <img src="{img_url}">
            {html_body}
            
            <div class="promo">
                 <h3 style="margin-top:0;">🛡️ Recommended Strategy</h3>
                 <p style="color:#666;">Hedge portfolio risk with physical assets.</p>
                 <a href="{amz_link}" style="background:#ff9900; color:white; padding:12px 25px; text-decoration:none; border-radius:8px; font-weight:bold; display:inline-block;">Check Gold Prices</a>
                 <div style="margin-top:15px;">
                    <a href="{BYBIT_LINK}" style="color:#333; font-weight:bold; font-size:0.9em;">Claim Trading Bonus →</a>
                 </div>
            </div>

            <div class="footer-card">
                <div style="font-size:3em; margin-bottom:10px;">🏛️</div>
                <h2 style="color:white; margin:0 0 10px 0;">Empire Analyst</h2>
                <p style="color:#888; margin-bottom:30px;">Automated Financial Intelligence System</p>
                <a href="{EMPIRE_URL}" class="btn">VISIT HEADQUARTERS →</a>
            </div>
        </body></html>
        """
        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
        log("✅ [블로그] index.html 업데이트 완료")
    except Exception as e: log(f"❌ HTML 저장 실패: {e}")

    # 4. Dev.to 업로드
    if DEVTO_TOKEN:
        try:
            log("🚀 [Dev.to] 업로드 시도...")
            requests.post("https://dev.to/api/articles", 
                headers={"api-key": DEVTO_TOKEN, "Content-Type": "application/json"}, 
                json={"article": {"title": topic, "published": True, "body_markdown": raw_md, "canonical_url": BLOG_BASE_URL}}, timeout=10)
        except Exception as e: log(f"⚠️ Dev.to 패스: {e}")

    # 5. X (트위터) 업로드
    if X_API_KEY:
        try:
            log("🐦 [X/Twitter] 업로드 시도...")
            client = tweepy.Client(X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET)
            client.create_tweet(text=f"⚡ Market Alert: {topic}\n\nFull analysis 👇\n{BLOG_BASE_URL}\n\n#Finance #Investing")
        except Exception as e: log(f"⚠️ X 패스: {e}")

if __name__ == "__main__":
    main()
