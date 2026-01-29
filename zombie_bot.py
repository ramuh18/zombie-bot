import os, json, random, requests, markdown, urllib.parse, feedparser, time, re
from datetime import datetime

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [환경변수]
def get_env(key):
    val = os.environ.get(key, "")
    if not val: return ""
    return val.strip().replace("\n", "").replace("\r", "")

GEMINI_API_KEY = get_env("GEMINI_API_KEY")
DEVTO_TOKEN = get_env("DEVTO_TOKEN")

# [사이트 설정]
BLOG_TITLE = "The Empire Analyst"
BLOG_DESC = "Global Financial Intelligence & Crypto Insights"
BLOG_BASE_URL = "https://ramuh18.github.io/zombie-bot/"
BYBIT_LINK = "https://www.bybit.com/invite?ref=DOVWK5A"
HISTORY_FILE = "history.json"

# ==========================================
# [1. 제목 세탁기]
# ==========================================
def clean_title_aggressive(text):
    text = text.strip().replace('"', '').replace("'", "").replace("*", "")
    patterns = [r"^BREAKING[:\s]*", r"^ALERT[:\s]*", r"^WARNING[:\s]*", r"^URGENT[:\s]*", r"Title:"]
    for p in patterns: text = re.sub(p, "", text, flags=re.IGNORECASE)
    return text.strip()

# ==========================================
# [2. 주제 선정]
# ==========================================
def get_hot_topic():
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        raw_news = random.choice(feed.entries[:5]).title if feed.entries else "Market Crash"
    except: raw_news = "Bitcoin Trend"

    prompt = f"""
    Rewrite this headline into a professional, engaging financial news title (MAX 10 WORDS).
    Original: "{raw_news}"
    Rules: No "BREAKING", no clickbait style. Sound like Bloomberg or WSJ.
    """
    
    title = "Market Update"
    for _ in range(2):
        try:
            if GEMINI_API_KEY:
                url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY
                resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=15)
                if resp.status_code == 200:
                    title = resp.json()['candidates'][0]['content']['parts'][0]['text']
                    break
            url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
            resp = requests.get(url, timeout=30)
            title = resp.text
            break
        except: time.sleep(1)
    return clean_title_aggressive(title)

# ==========================================
# [3. 히스토리 관리 (사이드바용)]
# ==========================================
def load_and_sync_history():
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f: history = json.load(f)
        except: pass
    if not history:
        try:
            resp = requests.get(f"{BLOG_BASE_URL}{HISTORY_FILE}", timeout=5)
            if resp.status_code == 200: history = resp.json()
        except: pass
    return history

def get_sidebar_recent_posts(history, current_title):
    html = "<ul class='recent-posts'>"
    count = 0
    for h in history:
        if h['title'] == current_title: continue
        full_url = f"{BLOG_BASE_URL}{h['file']}"
        html += f"<li><a href='{full_url}'>{h['title']}</a></li>"
        count += 1
        if count >= 5: break
    html += "</ul>"
    return html

# ==========================================
# [4. 본문 생성]
# ==========================================
def generate_part(topic, focus):
    prompt = f"Write a professional financial analysis section on '{topic}'. Focus: {focus}. Length: 350 words. Use Markdown (headers, bold). Tone: Analytical, Institutional."
    for _ in range(2):
        try:
            if GEMINI_API_KEY:
                url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY
                resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
                if resp.status_code == 200: return resp.json()['candidates'][0]['content']['parts'][0]['text']
            url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
            resp = requests.get(url, timeout=45)
            return resp.text
        except: time.sleep(1)
    return "Content generation pending..."

# ==========================================
# [5. HTML 템플릿 (에드센스 승인형)]
# ==========================================
def create_professional_html(topic, img_url, body_html, sidebar_html, canonical_url):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="In-depth analysis on {topic}. Global financial markets, crypto trends, and investment strategies.">
    <title>{topic} - {BLOG_TITLE}</title>
    <link rel="canonical" href="{canonical_url}" />
    <style>
        :root {{ --primary: #0a192f; --accent: #c0392b; --text: #333; --bg: #fdfdfd; }}
        body {{ font-family: 'Georgia', 'Times New Roman', serif; line-height: 1.8; color: var(--text); background: var(--bg); margin: 0; padding: 0; }}
        
        /* Header */
        header {{ background: var(--primary); color: #fff; padding: 20px 0; text-align: center; border-bottom: 5px solid var(--accent); }}
        .brand {{ font-size: 2.5rem; font-weight: bold; letter-spacing: -1px; margin: 0; font-family: 'Arial', sans-serif; }}
        .tagline {{ font-size: 0.9rem; opacity: 0.8; margin-top: 5px; font-family: sans-serif; }}
        
        /* Layout */
        .container {{ max-width: 1100px; margin: 30px auto; display: flex; flex-wrap: wrap; gap: 40px; padding: 0 20px; }}
        .main-content {{ flex: 2; min-width: 300px; }}
        .sidebar {{ flex: 1; min-width: 250px; background: #f8f9fa; padding: 25px; border-radius: 8px; height: fit-content; border-top: 3px solid var(--accent); }}
        
        /* Content Styling */
        h1 {{ font-size: 2.2rem; margin-top: 0; line-height: 1.2; }}
        h2 {{ font-family: 'Arial', sans-serif; color: var(--primary); margin-top: 30px; border-bottom: 1px solid #ddd; padding-bottom: 10px; }}
        .featured-img {{ width: 100%; height: auto; border-radius: 5px; margin-bottom: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }}
        a {{ color: var(--accent); text-decoration: none; font-weight: bold; }}
        a:hover {{ text-decoration: underline; }}
        
        /* Sidebar Styling */
        .widget h3 {{ font-family: 'Arial', sans-serif; font-size: 1.1rem; border-bottom: 2px solid #ddd; padding-bottom: 10px; margin-top: 0; }}
        .recent-posts {{ list-style: none; padding: 0; }}
        .recent-posts li {{ margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
        .recent-posts a {{ color: #555; font-size: 0.95rem; font-weight: normal; }}
        .ad-box {{ background: #000; color: #f1c40f; padding: 20px; text-align: center; border-radius: 5px; margin-top: 30px; }}
        
        /* Footer */
        footer {{ background: #111; color: #777; padding: 40px 0; text-align: center; margin-top: 50px; font-size: 0.9rem; }}
        
        @media (max-width: 768px) {{ .container {{ flex-direction: column; }} }}
    </style>
</head>
<body>

<header>
    <div class="brand">{BLOG_TITLE}</div>
    <div class="tagline">{BLOG_DESC}</div>
</header>

<div class="container">
    <main class="main-content">
        <article>
            <div style="font-size:0.85rem; color:#888; margin-bottom:10px;">MARKET ANALYSIS • {datetime.now().strftime("%B %d, %Y")}</div>
            <h1>{topic}</h1>
            <img src="{img_url}" class="featured-img" alt="{topic}">
            
            {body_html}
            
            <div style="margin-top:40px; padding:20px; background:#eef2f5; border-left:4px solid var(--primary);">
                <strong>📉 Trader's Note:</strong> This analysis is for informational purposes. 
                <a href="{BYBIT_LINK}">Check Live Charts on Bybit →</a>
            </div>
        </article>
    </main>

    <aside class="sidebar">
        <div class="widget">
            <h3>📂 Recent Reports</h3>
            {sidebar_html}
        </div>
        
        <div class="widget">
            <div class="ad-box">
                <div style="font-size:1.2rem; font-weight:bold; margin-bottom:10px;">🎁 $30,000 Bonus</div>
                <p style="font-size:0.9rem; color:#fff;">Exclusive for new traders</p>
                <a href="{BYBIT_LINK}" style="background:#f1c40f; color:#000; padding:8px 15px; display:inline-block; border-radius:4px; margin-top:5px;">Claim Now</a>
            </div>
        </div>
        
        <div class="widget" style="margin-top:30px;">
            <h3>🔍 Categories</h3>
            <ul class="recent-posts">
                <li><a href="#">Crypto Market</a></li>
                <li><a href="#">Stock Indices</a></li>
                <li><a href="#">Forex Strategy</a></li>
                <li><a href="#">Macroeconomics</a></li>
            </ul>
        </div>
    </aside>
</div>

<footer>
    <p>&copy; 2026 {BLOG_TITLE}. All Rights Reserved.</p>
    <p>Privacy Policy | Terms of Service | Contact</p>
</footer>

</body>
</html>"""

# ==========================================
# [6. 메인 실행]
# ==========================================
def main():
    log("🏁 봇 가동 시작 (Premium Theme)")
    topic = get_hot_topic()
    log(f"🔥 주제: {topic}")
    
    # 본문 3단 합체
    content = ""
    content += generate_part(topic, "Market Overview & Macro Data") + "\n\n"
    content += generate_part(topic, "Technical Analysis (Chart Patterns)") + "\n\n"
    content += generate_part(topic, "Investment Strategy & Risk Management")
    
    html_body = markdown.markdown(content)
    
    # 파일명 및 링크
    file_timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    archive_filename = f"post_{file_timestamp}.html"
    full_url = f"{BLOG_BASE_URL}{archive_filename}"
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('financial chart ' + topic)}"
    
    # 히스토리 동기화
    history = load_and_sync_history()
    sidebar_html = get_sidebar_recent_posts(history, topic)
    
    # 기록 저장
    new_entry = {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_filename}
    history.insert(0, new_entry)
    with open(HISTORY_FILE, "w") as f: json.dump(history, f, indent=4)
    
    # HTML 생성 (프리미엄 템플릿 사용)
    full_html = create_professional_html(topic, img_url, html_body, sidebar_html, full_url)
    
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_filename, "w", encoding="utf-8") as f: f.write(full_html)
    log("✅ 블로그 생성 완료")

    # Dev.to 업로드
    if DEVTO_TOKEN:
        try:
            dev_md = f"# {topic}\n\n![Cover]({img_url})\n\n{content}\n\n## 🔗 Read Full Analysis\n[Click here to read on our official site]({full_url})"
            payload = {"article": {"title": topic, "published": True, "body_markdown": dev_md, "tags": ["finance", "investing"], "canonical_url": full_url}}
            resp = requests.post("https://dev.to/api/articles", headers={"api-key": DEVTO_TOKEN}, json=payload, timeout=15)
            if resp.status_code in [200, 201]: log("✅ Dev.to 성공")
            else: log(f"❌ Dev.to 실패: {resp.status_code}")
        except: pass

if __name__ == "__main__": main()
