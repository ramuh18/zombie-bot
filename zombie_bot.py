import os, json, random, requests, markdown, urllib.parse, feedparser, tweepy, time, re
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [설정 로드 - 비밀번호 세척 강화]
def get_env(key):
    val = os.environ.get(key, "")
    if not val or "***" in val: return "" # 깃허브 마스킹이나 빈값 차단
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
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        if feed.entries: return feed.entries[0].title
    except: pass
    return "Global Market Volatility 2026"

# [2. 브루트포스 세척기 (외계어 박멸 핵심)]
def clean_text(raw_text):
    """JSON 찌꺼기를 현미경 수준으로 찾아내서 닦아내는 함수"""
    # 1. 텍스트 안에서 JSON 블록({ ... })만 추출 시도
    match = re.search(r'(\{.*\})', raw_text, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group(1))
            # 1순위: 'content' (진짜 본문)
            if 'content' in data: return data['content']
            # 2순위: 'reasoning_content' (사용자님 화면에 뜬 고민 내용)
            if 'reasoning_content' in data: return data['reasoning_content']
            # 3순위: 'choices' (OpenAI 스타일)
            if 'choices' in data: return data['choices'][0]['message']['content']
        except: pass

    # 2. JSON 파싱 실패 시: 정규식으로 직접 긁어오기
    for key in ['reasoning_content', 'content', 'message']:
        found = re.search(rf'"{key}"\s*:\s*"(.*?)"', raw_text, re.DOTALL)
        if found:
            return found.group(1).replace('\\n', '\n').replace('\\"', '"')

    # 3. 최후의 보루: 마크다운 헤더(#)부터 시작하는 부분만 남기기
    if '#' in raw_text:
        return raw_text[raw_text.find('#'):]

    return raw_text

# [3. 콘텐츠 엔진]
def generate_content(topic):
    log(f"🧠 {topic} 분석 중...")
    prompt = f"Write a 1000-word financial report about {topic}. Use Markdown. Tone: Professional Analyst."
    
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
    return f"# Market Alert: {topic}\n\nStrategic report is being updated."

# [4. 메인 실행]
def main():
    log("🏁 Empire Analyst Quantitative Bot v2.0 가동")
    topic = get_hot_topic()
    raw_md = generate_content(topic)
    keyword = "Finance"

    try:
        img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(topic + ' luxury finance 8k')}"
        amz_link = f"https://www.amazon.com/s?k=investment&tag={AMAZON_TAG}"
        
        html_body = markdown.markdown(raw_md)
        full_html = f"""
        <!DOCTYPE html>
        <html><head><title>Empire Analyst</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: sans-serif; max-width: 800px; margin: auto; padding: 40px 20px; line-height: 1.8; color: #333; }}
            img {{ width: 100%; border-radius: 16px; margin: 30px 0; }}
            .footer-card {{ background: #000; color: white; padding: 60px 30px; border-radius: 20px; text-align: center; margin-top: 80px; }}
            .footer-card a {{ color: white; font-weight: bold; border: 1px solid white; padding: 10px 20px; border-radius: 30px; text-decoration: none; }}
        </style></head>
        <body>
            <h1>{topic}</h1>
            <img src="{img_url}">
            {html_body}
            <div class="footer-card">
                <h2>Empire Analyst</h2>
                <a href="{EMPIRE_URL}">VISIT HEADQUARTERS →</a>
            </div>
        </body></html>
        """
        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
        log("✅ index.html 파일 저장 완료")
    except Exception as e: log(f"❌ HTML 저장 실패: {e}")

    # Dev.to 업로드 (에러 나도 무시하고 진행)
    if DEVTO_TOKEN:
        try:
            log("🚀 Dev.to 업로드 시도...")
            requests.post("https://dev.to/api/articles", headers={"api-key": DEVTO_TOKEN}, 
                          json={"article": {"title": topic, "published": True, "body_markdown": raw_md, "canonical_url": BLOG_BASE_URL}}, timeout=10)
        except: pass

    # X(트위터) 업로드 (에러 나도 무시하고 진행)
    if X_API_KEY:
        try:
            log("🐦 X 업로드 시도...")
            client = tweepy.Client(X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET)
            client.create_tweet(text=f"⚡ {topic}\n\nFull analysis here 👇\n{BLOG_BASE_URL}")
        except: pass

if __name__ == "__main__":
    main()
