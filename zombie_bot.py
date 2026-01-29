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
BLOG_TITLE = "Global Market Watch"
# ★ 사용자님 깃허브 주소 (마지막 슬래시 필수)
BLOG_BASE_URL = "https://ramuh18.github.io/zombie-bot/"

# [광고 설정]
EMPIRE_URL = "https://empire-analyst.digital/"
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_TAG = "empireanalyst-20"
AMAZON_LINK = f"https://www.amazon.com/s?k=ledger+nano+x&tag={AMAZON_TAG}"

HISTORY_FILE = "history.json"

# ==========================================
# [1. 제목 세탁기]
# ==========================================
def clean_title_aggressive(text):
    text = text.strip().replace('"', '').replace("'", "").replace("*", "")
    patterns = [r"^BREAKING[:\s]*", r"^ALERT[:\s]*", r"^WARNING[:\s]*", r"Title:"]
    for p in patterns: text = re.sub(p, "", text, flags=re.IGNORECASE)
    return text.strip()

# ==========================================
# [2. 주제 선정]
# ==========================================
def get_hot_topic():
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        raw_news = random.choice(feed.entries[:5]).title if feed.entries else "Bitcoin Analysis"
    except: raw_news = "Crypto Market Update"

    prompt = f"Rewrite '{raw_news}' into a professional financial news title (MAX 9 WORDS). No clickbait."
    
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
# [3. 히스토리 & 사이드바]
# ==========================================
def load_and_sync_history():
    history = []
    if os.path.exists(HISTORY_FILE):
        try: with open(HISTORY_FILE, "r") as f: history = json.load(f)
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
# [4. ★사이트맵 자동 생성기 (신규 기능)]
# ==========================================
def generate_sitemap(history):
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # 메인 페이지
    sitemap_xml += f'  <url><loc>{BLOG_BASE_URL}</loc><changefreq>daily</changefreq><priority>1.0</priority></url>\n'
    
    # 게시글들
    for h in history[:50]: # 최근 50개만
        url = f"{BLOG_BASE_URL}{h['file']}"
        date = h['date']
        sitemap_xml += f'  <url><loc>{url}</loc><lastmod>{date}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n'
        
    sitemap_xml += '</urlset>'
    
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_xml)
    log("🗺️ 사이트맵(sitemap.xml) 생성 완료")

# ==========================================
# [5. 본문 생성]
# ==========================================
def generate_part(topic, focus):
    prompt = f"Write a professional financial analysis section on '{topic}'. Focus: {focus}. Length: 350 words. Use Markdown. Tone: Institutional."
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
    return "Content generating..."

# ==========================================
# [6. HTML 템플릿 (SEO & 소셜 메타태그 추가)]
# ==========================================
def create_professional_html(topic, img_url, body_html, sidebar_html, canonical_url):
    # 나중에 구글 애널리틱스 ID를 받으면 'G-XXXXXXXXXX' 부분을 교체하세요.
    ga_script = """
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-XXXXXXXXXX');
    </script>
    """
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="In-depth financial analysis on {topic}. Institutional grade crypto and market insights.">
    <title>{topic} - {BLOG_TITLE}</title>
    <link rel="canonical" href="{canonical_url}" />
    
    <meta property="og:type" content="article" />
    <meta property="og:title" content="{topic}" />
    <meta property="og:description" content="Click to read full financial analysis and market outlook." />
    <meta property="og:image" content="{img_url}" />
    <meta property="og:url" content="{canonical_url}" />
    <meta name="twitter:card" content="summary_large_image" />

    <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@300;700&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {{ --primary: #0f172a; --accent: #dc2626; --bg: #ffffff; --text: #334155; --sidebar: #f1f5f9; }}
        body {{ font-family: 'Merriweather', serif; line-height: 1.8; color: var(--text); background: var(--bg); margin: 0; }}
        header {{ background: var(--primary); color: #fff; padding: 20px 0; border-bottom: 4px solid var(--accent); }}
        .header-wrap {{ max-width: 1100px; margin: 0 auto; padding: 0 20px; text-align: center; }}
        .brand {{ font-family: 'Roboto', sans-serif; font-size: 1.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }}
        .container {{ max-width: 1100px; margin: 40px auto; display: grid; grid-template-columns: 1fr; gap: 40px; padding: 0 20px; }}
        @media(min-width: 900px) {{ .container {{ grid-template-columns: 2.5fr 1fr; }} }}
        h1 {{ font-size: 2rem; color: #0f172a; line-height: 1.3; margin-top: 0; }}
        .featured-img {{ width: 100%; height: auto; border-radius: 6px; margin-bottom: 25px; }}
        .sidebar {{ background: var(--sidebar); padding: 25px; border-radius: 8px; height: fit-content; }}
        .ad-box {{ display: block; padding: 20px; border-radius: 6px; text-align: center; text-decoration: none; margin-bottom: 15px; transition: transform 0.2s; }}
        .ad-box:hover {{ transform: translateY(-3px); }}
        .ad-main {{ background: #0f172a; color: #fff; border: 2px solid #0f172a; }}
        .ad-affiliate {{ background: #fff; color: #000; border: 2px solid #f59e0b; }}
        .ad-amazon {{ background: #fff; color: #333; border: 2px solid #ea580c; }}
        .ad-title {{ display: block; font-weight: 700; font-size: 1.1rem; }}
        .ad-desc {{ display: block; font-size: 0.85rem; opacity: 0.9; }}
        a {{ color: var(--accent); text-decoration: none; font-weight: 700; }}
        .recent-posts {{ list-style: none; padding: 0; }}
        .recent-posts li {{ margin-bottom: 12px; border-bottom: 1px solid #e2e8f0; padding-bottom: 12px; }}
        footer {{ background: #0f172a; color: #94a3b8; text-align: center; padding: 40px 0; margin-top: 60px; font-size: 0.8rem; }}
    </style>
    </head>
<body>
<header><div class="header-wrap"><div class="brand">{BLOG_TITLE}</div></div></header>
<div class="container">
    <main>
        <article>
            <div style="font-size:0.8rem; color:#64748b; margin-bottom:15px; font-family:'Roboto',sans-serif;">MARKET INSIGHT • {datetime.now().strftime("%Y-%m-%d")}</div>
            <h1>{topic}</h1>
            <img src="{img_url}" class="featured-img" alt="{topic}">
            {body_html}
        </article>
    </main>
    <aside class="sidebar">
        <div class="widget">
            <h3 style="font-family:'Roboto',sans-serif;font-size:0.9rem;text-transform:uppercase;color:#64748b;border-bottom:1px solid #cbd5e1;padding-bottom:8px;margin-bottom:15px;">👑 Official Headquarters</h3>
            <a href="{EMPIRE_URL}" class="ad-box ad-main">
                <span class="ad-title">Empire Analyst HQ</span>
                <span class="ad-desc">Deep Dive Analysis & Premium Reports →</span>
            </a>
        </div>
        <div class="widget">
            <h3 style="font-family:'Roboto',sans-serif;font-size:0.9rem;text-transform:uppercase;color:#64748b;border-bottom:1px solid #cbd5e1;padding-bottom:8px;margin-bottom:15px;">🚀 Trading Bonus</h3>
            <a href="{AFFILIATE_LINK}" class="ad-box ad-affiliate">
                <span class="ad-title">💰 $30,000 Reward</span>
                <span class="ad-desc">Exclusive Sign-up Bonus</span>
            </a>
        </div>
        <div class="widget">
            <h3 style="font-family:'Roboto',sans-serif;font-size:0.9rem;text-transform:uppercase;color:#64748b;border-bottom:1px solid #cbd5e1;padding-bottom:8px;margin-bottom:15px;">🛡️ Secure Assets</h3>
            <a href="{AMAZON_LINK}" class="ad-box ad-amazon">
                <span class="ad-title">📦 Hardware Wallets</span>
                <span class="ad-desc">Buy Ledger/Trezor on Amazon</span>
            </a>
        </div>
        <div class="widget">
            <h3 style="font-family:'Roboto',sans-serif;font-size:0.9rem;text-transform:uppercase;color:#64748b;border-bottom:1px solid #cbd5e1;padding-bottom:8px;margin-bottom:15px;">📂 Recent News</h3>
            {sidebar_html}
        </div>
    </aside>
</div>
<footer>&copy; 2026 {BLOG_TITLE}. <a href="{EMPIRE_URL}" style="color:#cbd5e1;">Official Site</a></footer>
</body>
</html>"""

# ==========================================
# [7. 메인 실행]
# ==========================================
def main():
    log("🏁 봇 가동 (SEO Enhanced)")
    topic = get_hot_topic()
    log(f"🔥 주제: {topic}")
    
    content = ""
    content += generate_part(topic, "Macro Outlook") + "\n\n"
    content += generate_part(topic, "Technical Analysis") + "\n\n"
    content += generate_part(topic, "Actionable Strategy")
    html_body = markdown.markdown(content)
    
    file_timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    archive_filename = f"post_{file_timestamp}.html"
    full_url = f"{BLOG_BASE_URL}{archive_filename}"
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('financial chart ' + topic)}"
    
    history = load_and_sync_history()
    sidebar_html = get_sidebar_recent_posts(history, topic)
    
    new_entry = {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_filename}
    history.insert(0, new_entry)
    with open(HISTORY_FILE, "w") as f: json.dump(history, f, indent=4)
    
    # ★ 사이트맵 생성 실행
    generate_sitemap(history)
    
    full_html = create_professional_html(topic, img_url, html_body, sidebar_html, full_url)
    
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_filename, "w", encoding="utf-8") as f: f.write(full_html)
    log("✅ 블로그 생성 및 사이트맵 갱신 완료")

    if DEVTO_TOKEN:
        try:
            dev_md = f"# {topic}\n\n![Chart]({img_url})\n\n{content}\n\n## 🔗 More Insights\n[Visit Official Headquarters]({EMPIRE_URL})"
            payload = {"article": {"title": topic, "published": True, "body_markdown": dev_md, "tags": ["finance", "crypto"], "canonical_url": full_url}}
            requests.post("https://dev.to/api/articles", headers={"api-key": DEVTO_TOKEN}, json=payload, timeout=15)
            log("✅ Dev.to 성공")
        except: pass

if __name__ == "__main__": main()
