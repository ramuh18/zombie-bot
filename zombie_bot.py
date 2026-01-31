import os, json, random, requests, markdown, urllib.parse, time, re, sys, io
from datetime import datetime

# [SYSTEM] 한글 깨짐 방지
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [Configuration]
BLOG_TITLE = "Capital Insight" 
BLOG_BASE_URL = "https://ramuh18.github.io/capital-insight/" 
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = "https://www.amazon.com/s?k=ledger+nano+x&tag=empireanalyst-20"

# [📊 구글 트렌드 실시간 수집기]
def get_live_trends():
    try:
        url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
        resp = requests.get(url, timeout=15)
        titles = re.findall(r"<title>(.*?)</title>", resp.text)
        return titles[3:15] if len(titles) > 5 else ["Market Reset", "Global Inflation"]
    except:
        return ["Economic Supercycle", "Asset Sovereignty"]

# [🖋️ 1,500자급 고품질 리포트 엔진]
def generate_fixed_report(topic):
    templates = [
        f"""## Executive Summary: The Rise of {topic}
The 2026 financial markets are witnessing a tectonic shift driven by **{topic}**. This intelligence report examines the systemic implications and institutional responses to this emerging trend.

## 1. Macro-Indicators and Liquidity
The integration of {topic} into the broader economic discourse follows a period of extreme monetary expansion. As central banks tighten liquidity, {topic} has become a focal point for risk assessment. We observe a significant increase in institutional hedging strategies directly tied to {topic} volatility.

## 2. Strategic Asset Preservation
The primary risk associated with {topic} is the potential for systemic lockout within legacy banking institutions. We maintain that the only viable defense is the adoption of non-custodial storage solutions. Smart money is already migrating from exchange-based liabilities to hardware-secured sovereignty.

## 3. Final Conclusion
Monitoring {topic} is mandatory for any serious participant in the 2026 fiscal cycle. The transition toward a decentralized reserve architecture is accelerating. Prepare for the next phase of the supercycle by securing your assets today.""",

        f"""## Intelligence Alert: {topic} and Systemic Fragility
Our data nodes have intercepted a massive surge in capital flows related to **{topic}**. This movement suggests that institutional whales are repositioning for a major structural realignment.

## 1. The Death of Legacy Fiat
As inflation eats into the purchasing power of global reserves, {topic} represents a new frontier for value preservation. The correlation between {topic} and institutional debt is at an all-time high, signaling a lack of confidence in traditional paper assets.

## 2. Hard Asset Migration
The surge in {topic} interest coincides with record outflows from centralized banks. Investors are no longer willing to accept third-party risk. The migration to Cold Wallets is the ultimate signal of this new era of financial independence.

## 3. Tactical Recommendation
Do not be distracted by short-term volatility in {topic}. Focus on long-term accumulation and sovereign security. The reset is not coming; it is already here."""
    ]
    return random.choice(templates)

def create_final_html(topic, img_url, body_html, sidebar_html):
    # [디자인 복구 및 강화] 로고 그림자, 아마존 공지, 반응형 버튼
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic} | {BLOG_TITLE}</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;700&family=Oswald:wght@700&display=swap" rel="stylesheet">
    <style>
        :root {{ --main-blue: #001f3f; --accent-gold: #c5a059; --urgent-red: #d90429; }}
        body {{ font-family: 'Inter', sans-serif; background: #f8f9fa; color: #1a1a1a; line-height: 1.8; margin: 0; }}
        
        header {{ background: var(--main-blue); color: #fff; padding: 50px 20px; text-align: center; border-bottom: 8px solid var(--accent-gold); position: sticky; top:0; z-index:100; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }}
        .brand {{ font-family: 'Oswald', sans-serif; font-size: 3.5rem; letter-spacing: 4px; text-transform: uppercase; text-shadow: 3px 3px 0px var(--accent-gold); }}
        .tagline {{ font-size: 0.9rem; letter-spacing: 2px; color: var(--accent-gold); margin-top: 10px; font-weight: bold; }}

        .container {{ max-width: 1400px; margin: 50px auto; display: grid; grid-template-columns: 1fr 360px; gap: 50px; padding: 0 20px; }}
        @media(max-width: 1100px) {{ .container {{ grid-template-columns: 1fr; }} .sidebar {{ position: static; }} }}
        
        main {{ background: #fff; padding: 50px; border-radius: 4px; box-shadow: 0 10px 40px rgba(0,0,0,0.05); border: 1px solid #eee; }}
        h1 {{ font-family: 'Playfair Display', serif; color: var(--main-blue); font-size: 3.5rem; line-height: 1.1; margin-top: 0; margin-bottom: 30px; }}
        img {{ width: 100%; height: auto; border-radius: 4px; margin-bottom: 40px; border: 1px solid #ddd; filter: contrast(1.1); }}
        
        .content {{ font-size: 1.25rem; color: #333; }}
        .content h2 {{ color: var(--main-blue); border-left: 5px solid var(--accent-gold); padding-left: 20px; margin-top: 60px; font-family: 'Oswald'; }}
        
        .side-card {{ background: #fff; padding: 30px; border-radius: 4px; margin-bottom: 30px; border-top: 6px solid var(--main-blue); box-shadow: 0 5px 20px rgba(0,0,0,0.05); }}
        .btn {{ display: block; padding: 20px; background: var(--main-blue); color: #fff; text-decoration: none; font-weight: bold; text-align: center; margin-bottom: 15px; border-radius: 4px; transition: 0.3s; font-size: 1.1rem; border: 1px solid transparent; }}
        .btn-red {{ background: var(--urgent-red); }}
        .btn:hover {{ background: #fff; color: var(--main-blue); border: 1px solid var(--main-blue); transform: translateY(-3px); }}
        
        .amazon-notice {{ font-size: 0.8rem; color: #999; line-height: 1.4; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee; font-style: italic; }}
        footer {{ text-align: center; padding: 100px 20px; color: #666; background: #fff; border-top: 1px solid #eee; }}
    </style></head>
    <body>
    <header>
        <div class="brand">{BLOG_TITLE}</div>
        <div class="tagline">STRATEGIC FINANCIAL INTELLIGENCE UNIT</div>
    </header>
    <div class="container">
        <main>
            <div style="color:var(--urgent-red); font-weight:bold; margin-bottom:10px; letter-spacing:1px;">[ MARKET TREND ADVISORY ]</div>
            <h1>{topic}</h1>
            <img src="{img_url}">
            <div class="content">{body_html}</div>
        </main>
        <aside class="sidebar">
            <div class="side-card">
                <a href="{EMPIRE_URL}" class="btn btn-red">🔴 ACCESS EXIT PLAN</a>
                <a href="{AFFILIATE_LINK}" class="btn">📉 SHORT MARKET</a>
                <a href="{AMAZON_LINK}" class="btn">🛡️ SECURE ASSETS (Ledger)</a>
            </div>
            <div class="side-card">
                <h3 style="margin-top:0; color:var(--main-blue); font-family:'Oswald'; border-bottom:3px solid var(--accent-gold); padding-bottom:10px;">LATEST SIGNALS</h3>
                <ul style="list-style:none; padding:0; line-height:2.5; font-size:1rem;">{sidebar_html}</ul>
            </div>
            <div class="amazon-notice">
                * As an Amazon Associate, this site earns from qualifying purchases. This helps support our independent market research.
            </div>
        </aside>
    </div>
    <footer>
        &copy; 2026 {BLOG_TITLE}. All Rights Reserved.<br>
        Unauthorized reproduction is strictly prohibited under Strategic Intelligence Protocols.
    </footer></body></html>"""

def main():
    trends = get_live_trends()
    topic = random.choice(trends)
    body_text = generate_fixed_report(topic)
    html_body = markdown.markdown(body_text)
    
    # 이미지 스타일을 더 고급스럽게 변경 (추상적이고 명암이 확실한 차트)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('high-end luxury financial office dark blue gold accent abstract 8k stock market chart photography')}?width=1200&height=600"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = "".join([f"<li><b style='color:var(--accent-gold);'>▶</b> <a href='{BLOG_BASE_URL}{h.get('file','')}' style='color:#333; text-decoration:none;'>{h.get('title')[:25]}...</a></li>" for h in history[:10]])
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_final_html(topic, img_url, html_body, sidebar_html)
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)

if __name__ == "__main__": main()
