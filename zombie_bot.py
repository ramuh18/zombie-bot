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

# [★브랜드 리브랜딩: 좀비 봇 흔적 지우기]
# URL은 zombie-bot이어도, 보여지는 이름은 'Empire Market Intelligence'입니다.
BLOG_TITLE = "Empire Market Intelligence"
BLOG_DESC = "Daily Crypto & Global Finance Briefing"
BLOG_BASE_URL = "https://ramuh18.github.io/zombie-bot/"

# [수익화 설정]
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

    prompt = f"Rewrite '{raw_news}' into a high-end financial newsletter title (MAX 9 WORDS). Professional, trustworthy tone."
    
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
# [3. 히스토리 & 사이트맵 & 아카이브]
# ==========================================
def load_and_sync_history():
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        except: pass
    if not history:
        try:
            resp = requests.get(f"{BLOG_BASE_URL}{HISTORY_FILE}", timeout=5)
            if resp.status_code == 200: history = resp.json()
        except: pass
    return history

def generate_sitemap(history):
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap_xml += f'  <url><loc>{BLOG_BASE_URL}</loc><changefreq>daily</changefreq><priority>1.0</priority></url>\n'
    for h in history[:100]:
        url = f"{BLOG_BASE_URL}{h['file']}"
        date = h['date']
        sitemap_xml += f'  <url><loc>{url}</loc><lastmod>{date}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n'
    sitemap_xml += '</urlset>'
    with open("sitemap.xml", "w", encoding="utf-8") as f: f.write(sitemap_xml)

def generate_archive_page(history):
    list_html = ""
    for h in history:
        full_url = f"{BLOG_BASE_URL}{h['file']}"
        list_html += f"""
        <div style="margin-bottom:20px; padding-bottom:15px; border-bottom:1px solid #eee;">
            <div style="font-size:0.8rem; color:#888;">{h['date']}</div>
            <a href="{full_url}" style="font-size:1.1rem; font-weight:bold; text-decoration:none; color:#333;">{h['title']}</a>
        </div>
        """
    archive_html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Archive - {BLOG_TITLE}</title><style>body{{font-family:'Merriweather',serif;line-height:1.6;max-width:800px;margin:0 auto;padding:20px;color:#333;}}h1{{border-bottom:4px solid #0f172a;padding-bottom:10px;}}a:hover{{color:#dc2626;}}.btn{{display:inline-block;margin-top:20px;background:#0f172a;color:#fff;padding:10px 20px;text-decoration:none;border-radius:4px;}}</style></head><body><h1>📂 Intelligence Archive</h1>{list_html}<a href="index.html" class="btn">← Back to Briefing</a></body></html>"""
    with open("archive.html", "w", encoding="utf-8") as f: f.write(archive_html)

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
    html += f"<div style='margin-top:15px; text-align:right;'><a href='{BLOG_BASE_URL}archive.html' style='font-size:0.85rem; color:#dc2626; font-weight:bold;'>📂 View Full Archive →</a></div>"
    return html

# ==========================================
# [4. 본문 생성]
# ==========================================
def generate_part(topic, focus):
    prompt = f"Write a professional financial newsletter section on '{topic}'. Focus: {focus}. Length: 350 words. Use Markdown. Tone: Institutional, Analytical, Trustworthy."
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
    return "Analyzing market data..."

# ==========================================
# [5. HTML 템플릿 (신뢰도 & 법적 면책 강화)]
# ==========================================
def create_professional_html(topic, img_url, body_html, sidebar_html, canonical_url):
    google_verification = '<meta name="google-site-verification" content="Jxh9S9J3S5_RBIpJH4CVrDkpRiDZ_mQ99TfIm7xK7YY" />'
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    {google_verification}
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Daily financial briefing on {topic}. Empire Market Intelligence provided by advanced analysis.">
    <title>{topic} | {BLOG_TITLE}</title>
    <link rel="canonical" href="{canonical_url}" />
    
    <meta property="og:type" content="article" />
    <meta property="og:title" content="{topic}" />
    <meta property="og:description" content="Read the full daily briefing." />
    <meta property="og:image" content="{img_url}" />
    <meta property="og:url" content="{canonical_url}" />
    <meta name="twitter:card" content="summary_large_image" />

    <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@300;700;900&family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {{ --primary: #0f172a; --accent: #b91c1c; --bg: #ffffff; --text: #334155; --sidebar: #f8fafc; }}
        body {{ font-family: 'Merriweather', serif; line-height: 1.8; color: var(--text); background: var(--bg); margin: 0; }}
        
        /* 뉴스레터 스타일 헤더 */
        header {{ background: var(--primary); color: #fff; padding: 25px 0; border-bottom: 5px solid var(--accent); }}
        .header-wrap {{ max-width: 1100px; margin: 0 auto; padding: 0 20px; text-align: center; }}
        .brand {{ font-family: 'Roboto', sans-serif; font-size: 2.2rem; font-weight: 900; text-transform: uppercase; letter-spacing: 1px; line-height: 1.2; }}
        .sub-brand {{ font-family: 'Roboto', sans-serif; font-size: 0.9rem; font-weight: 400; opacity: 0.8; margin-top: 5px; letter-spacing: 2px; }}
        .date-badge {{ display: inline-block; background: var(--accent); color: #fff; padding: 4px 12px; border-radius: 20px; font-family: 'Roboto', sans-serif; font-size: 0.8rem; font-weight: bold; margin-top: 15px; }}

        .container {{ max-width: 1100px; margin: 40px auto; display: grid; grid-template-columns: 1fr; gap: 50px; padding: 0 20px; }}
        @media(min-width: 900px) {{ .container {{ grid-template-columns: 2.4fr 1fr; }} }}
        
        h1 {{ font-size: 2.4rem; color: #0f172a; line-height: 1.25; margin-top: 0; font-weight: 900; }}
        .meta-info {{ font-family: 'Roboto', sans-serif; font-size: 0.85rem; color: #64748b; margin-bottom: 20px; font-weight: 500; text-transform: uppercase; }}
        
        .featured-img {{ width: 100%; height: auto; border-radius: 8px; margin-bottom: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
        
        /* 사이드바 & 광고 */
        .sidebar {{ background: var(--sidebar); padding: 30px; border-radius: 12px; height: fit-content; border: 1px solid #e2e8f0; }}
        .widget {{ margin-bottom: 40px; }}
        .widget h3 {{ font-family: 'Roboto', sans-serif; font-size: 0.85rem; text-transform: uppercase; color: #94a3b8; letter-spacing: 1px; border-bottom: 2px solid #cbd5e1; padding-bottom: 8px; margin-bottom: 20px; font-weight: 700; }}
        
        .ad-box {{ display: block; padding: 25px 20px; border-radius: 8px; text-align: center; text-decoration: none; margin-bottom: 15px; transition: all 0.2s; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
        .ad-box:hover {{ transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
        .ad-main {{ background: #0f172a; color: #fff; border: 1px solid #0f172a; }}
        .ad-affiliate {{ background: #ffffff; color: #0f172a; border: 2px solid #f59e0b; }}
        .ad-amazon {{ background: #ffffff; color: #0f172a; border: 2px solid #ea580c; }}
        .ad-title {{ display: block; font-weight: 900; font-size: 1.2rem; font-family: 'Roboto', sans-serif; margin-bottom: 5px; }}
        .ad-desc {{ display: block; font-size: 0.9rem; opacity: 0.9; }}

        a {{ color: var(--accent); text-decoration: none; font-weight: 700; }}
        .recent-posts li {{ margin-bottom: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 15px; }}
        
        footer {{ background: #0f172a; color: #64748b; text-align: center; padding: 50px 0; margin-top: 80px; font-size: 0.8rem; font-family: 'Roboto', sans-serif; }}
        .disclaimer {{ max-width: 800px; margin: 20px auto; line-height: 1.6; opacity: 0.7; font-size: 0.75rem; }}
    </style>
</head>
<body>
<header>
    <div class="header-wrap">
        <div class="brand">{BLOG_TITLE}</div>
        <div class="sub-brand">{BLOG_DESC}</div>
        <div class="date-badge">📅 DAILY BRIEFING #{current_date}</div>
    </div>
</header>
<div class="container">
    <main>
        <article>
            <div class="meta-info">Global Markets • Crypto • {current_date}</div>
            <h1>{topic}</h1>
            <img src="{img_url}" class="featured-img" alt="{topic}">
            {body_html}
            <div style="margin-top:40px; padding:20px; background:#f1f5f9; border-left:4px solid var(--primary); font-size:0.9rem;">
                <strong>💡 Editor's Note:</strong> This briefing is generated for informational purposes. Always do your own research.
                <br>Bookmark this page (Ctrl+D) to get daily market intelligence.
            </div>
        </article>
    </main>
    <aside class="sidebar">
        <div class="widget">
            <h3>👑 Official Headquarters</h3>
            <a href="{EMPIRE_URL}" class="ad-box ad-main">
                <span class="ad-title">Empire Analyst HQ</span>
                <span class="ad-desc">Get Full Institutional Reports & Deep Dive Analysis →</span>
            </a>
        </div>
        <div class="widget">
            <h3>🚀 Limited Offer</h3>
            <a href="{AFFILIATE_LINK}" class="ad-box ad-affiliate">
                <span class="ad-title">💰 $30,000 Bonus</span>
                <span class="ad-desc">Exclusive Sign-up Reward for New Traders</span>
            </a>
        </div>
        <div class="widget">
            <h3>🛡️ Security Essentials</h3>
            <a href="{AMAZON_LINK}" class="ad-box ad-amazon">
                <span class="ad-title">📦 Hardware Wallets</span>
                <span class="ad-desc">Secure Your Crypto with Ledger (Amazon Official)</span>
            </a>
        </div>
        <div class="widget">
            <h3>📂 Recent Intelligence</h3>
            {sidebar_html}
        </div>
    </aside>
</div>
<footer>
    <div>&copy; 2026 {BLOG_TITLE}. All rights reserved.</div>
    <div class="disclaimer">
        <strong>Affiliate & Amazon Disclaimer:</strong><br>
        {BLOG_TITLE} is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com. As an Amazon Associate I earn from qualifying purchases.
        <br>Some links on this page may be affiliate links.
    </div>
    <br><a href="{EMPIRE_URL}" style="color:#94a3b8; text-decoration:underline;">Visit Official Website</a>
</footer>
</body>
</html>"""

# ==========================================
# [6. 메인 실행]
# ==========================================
def main():
    log("🏁 봇 가동 (Trust & Compliance Upgrade)")
    topic = get_hot_topic()
    log(f"🔥 주제: {topic}")
    
    content = ""
    content += generate_part(topic, "Macro Outlook") + "\n\n"
    content += generate_part(topic, "Technical Analysis") + "\n\n"
    content += generate_part(topic, "Strategic Action")
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
    
    generate_sitemap(history)
    generate_archive_page(history)
    
    full_html = create_professional_html(topic, img_url, html_body, sidebar_html, full_url)
    
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_filename, "w", encoding="utf-8") as f: f.write(full_html)
    log("✅ 생성 완료")

    if DEVTO_TOKEN:
        try:
            dev_md = f"# {topic}\n\n![Chart]({img_url})\n\n{content}\n\n## 🔗 Full Briefing\n[Read on Empire Market Intelligence]({full_url})"
            payload = {"article": {"title": topic, "published": True, "body_markdown": dev_md, "tags": ["finance", "crypto"], "canonical_url": full_url}}
            requests.post("https://dev.to/api/articles", headers={"api-key": DEVTO_TOKEN}, json=payload, timeout=15)
            log("✅ Dev.to 성공")
        except: pass

if __name__ == "__main__": main()
