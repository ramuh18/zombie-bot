import os, json, random, requests, markdown, urllib.parse, time, re, sys, io
from datetime import datetime

# [SYSTEM]
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [Configuration]
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
BLOG_TITLE = "Capital Insight" 
BLOG_BASE_URL = "https://ramuh18.github.io/capital-insight/" 
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")

# 수익화 링크 복구
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = "https://www.amazon.com/s?k=ledger+nano+x&tag=empireanalyst-20"

def get_google_trends():
    try:
        url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
        resp = requests.get(url, timeout=20)
        titles = re.findall(r"<title>(.*?)</title>", resp.text)
        return titles[3:13] if len(titles) > 5 else ["Global Market Reset", "Interest Rate Shift"]
    except:
        return ["Economic Supercycle", "Market Liquidity"]

def generate_report(topic):
    prompt = f"Write a professional 1500-word financial report on '{topic}'. Tone: Institutional. English Only. Markdown."
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.6, "maxOutputTokens": 1800}}, timeout=40)
        return resp.json()['candidates'][0]['content']['parts'][0]['text'].strip()
    except:
        return f"# Analysis: {topic}\n\nThe current trend of **{topic}** is reshaping the 2026 fiscal landscape. Institutional shifts are becoming more apparent as liquidity tightens..."

def create_final_html(topic, img_url, body_html, sidebar_html):
    # 상단 로고(header)와 사이드바 버튼(side-card) 디자인 복구
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Oswald:wght@700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; background: #f4f7f9; color: #333; line-height: 1.8; margin: 0; }}
        header {{ background: #003366; color: white; padding: 30px; text-align: center; border-bottom: 5px solid #00509d; }}
        .brand {{ font-family: 'Oswald', sans-serif; font-size: 2.5rem; letter-spacing: 2px; text-transform: uppercase; }}
        
        .container {{ max-width: 1300px; margin: 40px auto; display: grid; grid-template-columns: 1fr 340px; gap: 40px; padding: 0 20px; }}
        @media(max-width: 1100px) {{ .container {{ grid-template-columns: 1fr; }} .sidebar {{ position: static; }} }}
        
        main {{ background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        h1 {{ color: #003366; font-size: 3rem; line-height: 1.1; margin-top: 0; }}
        img {{ width: 100%; height: 500px; object-fit: cover; border-radius: 8px; margin-bottom: 30px; }}
        
        .sidebar {{ background: transparent; }}
        .side-card {{ background: #fff; padding: 25px; border-radius: 8px; border-top: 5px solid #003366; margin-bottom: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }}
        .btn {{ display: block; padding: 18px; background: #003366; color: white; text-align: center; text-decoration: none; font-weight: bold; margin-bottom: 12px; border-radius: 4px; transition: 0.3s; }}
        .btn-red {{ background: #e60000; }}
        .btn:hover {{ filter: brightness(1.2); }}
        
        footer {{ text-align: center; padding: 80px 20px; color: #888; border-top: 1px solid #ddd; margin-top: 60px; }}
    </style></head>
    <body>
    <header><div class="brand">{BLOG_TITLE}</div></header>
    <div class="container">
        <main><h1>{topic}</h1><img src="{img_url}"><div class="content">{body_html}</div></main>
        <aside class="sidebar">
            <div class="side-card">
                <a href="{EMPIRE_URL}" class="btn btn-red">🛑 ACCESS FULL INTEL</a>
                <a href="{AFFILIATE_LINK}" class="btn">📉 SHORT MARKET</a>
                <a href="{AMAZON_LINK}" class="btn">🛡️ SECURE ASSETS (Ledger)</a>
            </div>
            <div class="side-card">
                <h3 style="margin-top:0; color:#003366; border-bottom:2px solid #003366;">TRENDING NOW</h3>
                <ul style="list-style:none; padding:0; line-height:2.2; font-size:0.9rem;">{sidebar_html}</ul>
            </div>
        </aside>
    </div>
    <footer>&copy; 2026 {BLOG_TITLE} | Amazon Associate Disclaimer included.</footer></body></html>"""

def main():
    log("⚡ Rebuilding UI with Trend Logic...")
    trends = get_google_trends()
    topic = random.choice(trends)
    full_text = generate_report(topic)
    html_body = markdown.markdown(full_text)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('professional finance blue dark 8k photography')}?width=1200&height=500"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = "".join([f"<li><a href='{BLOG_BASE_URL}{h.get('file','')}' style='color:#333; text-decoration:none;'>[{h.get('date')}] {h.get('title')[:25]}...</a></li>" for h in history[:10]])
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_final_html(topic, img_url, html_body, sidebar_html)
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)
    log(f"✅ Recovery Complete: {topic}")

if __name__ == "__main__": main()
