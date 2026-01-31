import os, json, random, requests, markdown, urllib.parse, time, re, sys, io
from datetime import datetime

# [SYSTEM] 환경 설정
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# [Configuration] ★각 호기별로 여기만 수정하세요★
BLOG_TITLE = "Capital Insight" 
BLOG_BASE_URL = "https://ramuh18.github.io/capital-insight/" 
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = "https://www.amazon.com/s?k=ledger+nano+x&tag=empireanalyst-20"

# [📊 구글 트렌드 실시간 수집기] - API 없이 RSS로 작동
def get_live_trends():
    try:
        url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
        resp = requests.get(url, timeout=15)
        titles = re.findall(r"<title>(.*?)</title>", resp.text)
        return titles[3:15] if len(titles) > 5 else ["Market Reset", "Global Inflation"]
    except:
        return ["Economic Supercycle", "Asset Sovereignty"]

# [🖋️ 1,500자급 고품질 리포트 엔진] - API 없이 자체 생성
def generate_fixed_report(topic):
    # 각기 다른 구성의 전문 템플릿 3종 중 랜덤 선택
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
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic} | {BLOG_TITLE}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Oswald:wght@700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; background: #f4f7f9; color: #1a1a1a; line-height: 1.8; margin: 0; }}
        header {{ background: #002d5b; color: #fff; padding: 35px; text-align: center; border-bottom: 6px solid #e60000; position: sticky; top:0; z-index:100; }}
        .brand {{ font-family: 'Oswald', sans-serif; font-size: 2.8rem; letter-spacing: 3px; }}
        .container {{ max-width: 1300px; margin: 50px auto; display: grid; grid-template-columns: 1fr 350px; gap: 45px; padding: 0 20px; }}
        @media(max-width: 1100px) {{ .container {{ grid-template-columns: 1fr; }} .sidebar {{ position: static; }} }}
        main {{ background: #fff; padding: 45px; border-radius: 10px; box-shadow: 0 5px 25px rgba(0,0,0,0.05); }}
        h1 {{ color: #002d5b; font-size: 3rem; line-height: 1.1; margin-top: 0; }}
        img {{ width: 100%; height: auto; border-radius: 8px; margin-bottom: 35px; border: 1px solid #eee; }}
        .side-card {{ background: #fff; padding: 25px; border-radius: 10px; margin-bottom: 25px; border-top: 5px solid #002d5b; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        .btn {{ display: block; padding: 18px; background: #002d5b; color: #fff; text-decoration: none; font-weight: bold; text-align: center; border-radius: 5px; margin-bottom: 12px; }}
        .btn-red {{ background: #e60000; }}
        footer {{ text-align: center; padding: 80px; color: #777; background: #fff; border-top: 1px solid #eee; }}
    </style></head>
    <body>
    <header><div class="brand">{BLOG_TITLE}</div></header>
    <div class="container">
        <main>
            <div style="color:#e60000; font-weight:bold; margin-bottom:10px;">[ LIVE TREND ANALYSIS ]</div>
            <h1>{topic}</h1>
            <img src="{img_url}">
            <div class="content">{body_html}</div>
        </main>
        <aside class="sidebar">
            <div class="side-card">
                <a href="{EMPIRE_URL}" class="btn btn-red">🛑 ACCESS FULL INTEL</a>
                <a href="{AFFILIATE_LINK}" class="btn">📉 SHORT MARKET</a>
                <a href="{AMAZON_LINK}" class="btn">🛡️ SECURE ASSETS</a>
            </div>
            <div class="side-card">
                <h3 style="margin-top:0; color:#002d5b; border-bottom:2px solid #e60000;">TRENDING NOW</h3>
                <ul style="list-style:none; padding:0; line-height:2.2; font-size:0.95rem;">{sidebar_html}</ul>
            </div>
        </aside>
    </div>
    <footer>&copy; 2026 {BLOG_TITLE}</footer></body></html>"""

def main():
    trends = get_live_trends()
    topic = random.choice(trends)
    body_text = generate_fixed_report(topic)
    html_body = markdown.markdown(body_text)
    
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('professional financial data abstract blue red 8k')}?width=1200&height=600"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = "".join([f"<li><b style='color:#e60000;'>!</b> <a href='{BLOG_BASE_URL}{h.get('file','')}' style='color:#333; text-decoration:none;'>{h.get('title')[:25]}...</a></li>" for h in history[:10]])
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_final_html(topic, img_url, html_body, sidebar_html)
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)

if __name__ == "__main__": main()
