import os, json, random, requests, markdown, urllib.parse, time, re, sys, io
from datetime import datetime

# [SYSTEM] 환경 설정
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# [Configuration]
BLOG_TITLE = "Capital Insight" 
BLOG_BASE_URL = "https://ramuh18.github.io/capital-insight/" 
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")
# [수익화 핵심] 본문 중간에 삽입할 제휴 링크
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = "https://www.amazon.com/s?k=ledger+nano+x&tag=empireanalyst-20"

# [주제 리스트: 사람들의 '돈 걱정'을 자극하는 키워드 위주]
BACKUP_TOPICS = [
    "The Collapse of Fiat Currency", "Why Your Savings Are Dying", "The Next Great Depression",
    "Hyperinflation Warning Signs", "Bank Bail-ins Explained", "The End of the Dollar",
    "CBDC: Total Surveillance", "Protecting Wealth from Confiscation", "The Retirement Crisis",
    "Housing Market Crash 2026", "The Truth About Inflation", "Wall Street's Secret Exit",
    "Prepare for the Reset", "Wealth Transfer Events", "Escaping the Rat Race",
    "Financial Freedom Protocols", "The Debt Supercycle Burst", "Gold vs Digital Gold",
    "Surviving the Credit Crunch", "The Middle Class Squeeze", "Taxation and Wealth Control",
    "Offshore Wealth Strategies", "The Liquidity Trap", "Pension Fund Insolvency",
    "Global Currency War", "The Rise of Hard Assets", "De-Banking Risks",
    "Smart Money Movements", "Technocratic Control", "Energy Crisis Survival",
    "Food Inflation Hedge", "Precious Metals Manipulation", "Real Estate Trap",
    "Stock Market Bubble Pop", "The Bond Market Collapse", "Derivatives Time Bomb",
    "Safe Haven Scarcity", "Institutional Accumulation", "Retail Investor Slaughter",
    "Algorithm Trading Risks", "The Cashless Society Danger", "Sovereign Individual Thesis",
    "Digital Asset Security", "The Great Wealth Gap", "Zombie Companies Crash",
    "Stagflation Nightmare", "Deflationary Depression", "The Money Printer Fallacy",
    "Capital Controls Coming", "Exit Strategies for 2026"
]

def get_live_trends():
    selected_topic = random.choice(BACKUP_TOPICS)
    return [selected_topic]

# [핵심 수정: 교육이 아니라 '행동(클릭)'을 유도하는 선동형 카피라이팅]
def generate_deep_report(topic):
    return f"""
# [URGENT_WARNING] Why {topic} Should Terrify You

## 1. The Silent Robbery
Most people are sleeping while **{topic}** is quietly eroding their financial future. The mainstream media tells you everything is fine, but the data on {topic} suggests a catastrophic shift is underway. If you are holding traditional assets or keeping cash in the bank, you are the primary victim of this systemic failure. **The system is not broken; it was built to take your wealth.**

## 2. The Trap is Set
Institutional whales have already positioned themselves to profit from **{topic}**. They are exiting the burning building while telling retail investors to "buy the dip." When the full impact of {topic} hits the markets, liquidity will dry up instantly. The doors will close, and your capital will be locked inside the legacy system. This is not a prediction; it is a mathematical certainty based on current leverage ratios.

> **[CRITICAL ALERT]** Do not leave your assets vulnerable. The window to act is closing.  
> <a href="{AFFILIATE_LINK}" style="color: red; font-weight: bold;">>> CLICK HERE TO HEDGE YOUR PORTFOLIO NOW</a>

## 3. Your Only Escape Route
There is only one way to survive the fallout of **{topic}**: Radical Sovereignty. You must decouple your wealth from the debt-based fiat system immediately. This means moving into hard assets and self-custody solutions that cannot be frozen, seized, or inflated away.

* **Step 1:** Stop trusting banks with your life savings.
* **Step 2:** Accumulate sovereign assets. <a href="{AMAZON_LINK}" style="text-decoration: underline;">[Get Hardware Security Here]</a>
* **Step 3:** Bet against the collapsing system.

## 4. Final Verdict
The timeline for **{topic}** is accelerating. You have two choices: watch your purchasing power vanish, or take action today to secure your financial freedom. History favors the prepared. Do not be part of the herd that gets slaughtered.

<div style="background: #eee; padding: 15px; border-left: 5px solid #d90429; margin-top: 20px;">
    <strong>🚀 ACTION REQUIRED:</strong> The markets are moving fast. 
    <a href="{EMPIRE_URL}"><strong>[ACCESS THE FULL STRATEGY GUIDE AT EMPIRE ANALYST]</strong></a>
</div>
"""

def generate_seo_files(history):
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += f'  <url><loc>{BLOG_BASE_URL}</loc><priority>1.0</priority></url>\n'
    for h in history[:50]:
        sitemap += f'  <url><loc>{BLOG_BASE_URL}{h["file"]}</loc><priority>0.8</priority></url>\n'
    sitemap += '</urlset>'
    with open("sitemap.xml", "w", encoding="utf-8") as f: f.write(sitemap)
    robots = f"User-agent: *\nAllow: /\nSitemap: {BLOG_BASE_URL}sitemap.xml"
    with open("robots.txt", "w", encoding="utf-8") as f: f.write(robots)

def create_final_html(topic, img_url, body_html, sidebar_html):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google-site-verification" content="여기에_인증태그_입력" />
    <title>WARNING: {topic} | {BLOG_TITLE}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Oswald:wght@700&display=swap" rel="stylesheet">
    <style>
        :root {{ --main-blue: #001f3f; --accent-gold: #c5a059; --alert-red: #d90429; }}
        body {{ font-family: 'Inter', sans-serif; background: #f0f2f5; color: #1a1a1a; line-height: 1.8; margin: 0; }}
        header {{ background: var(--main-blue); color: #fff; padding: 25px; text-align: center; border-bottom: 5px solid var(--alert-red); }}
        .brand {{ font-family: 'Oswald', sans-serif; font-size: 2.5rem; letter-spacing: 1px; text-transform: uppercase; color: #fff; }}
        .container {{ max-width: 1300px; margin: 30px auto; display: grid; grid-template-columns: 1fr 340px; gap: 40px; padding: 0 20px; }}
        @media(max-width: 1000px) {{ .container {{ grid-template-columns: 1fr; }} }}
        main {{ background: #fff; padding: 45px; border-radius: 8px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); border: 1px solid #ddd; }}
        h1 {{ color: var(--alert-red); font-family: 'Oswald', sans-serif; font-size: 2.8rem; line-height: 1.2; text-transform: uppercase; }}
        .content h2 {{ color: var(--main-blue); font-family: 'Oswald'; margin-top: 40px; border-left: 6px solid var(--accent-gold); padding-left: 15px; font-size: 1.8rem; }}
        img {{ width: 100%; height: auto; border-radius: 4px; margin-bottom: 30px; border: 1px solid #ccc; }}
        .side-card {{ background: #fff; padding: 25px; border-top: 5px solid var(--main-blue); box-shadow: 0 5px 15px rgba(0,0,0,0.05); margin-bottom: 20px; border-radius: 4px; }}
        .btn {{ display: block; padding: 18px; background: var(--alert-red); color: #fff; text-decoration: none; font-weight: bold; text-align: center; margin-bottom: 12px; border-radius: 6px; font-size: 1.1rem; transition: transform 0.2s; }}
        .btn:hover {{ transform: scale(1.02); background: #b00020; }}
        footer {{ text-align: center; padding: 60px; color: #777; border-top: 1px solid #ddd; background: #fff; margin-top: 40px; }}
        .footer-links a {{ color: #555; text-decoration: none; margin: 0 10px; cursor: pointer; }}
        .amazon-disclaimer {{ font-size: 0.75rem; color: #aaa; margin-top: 15px; font-style: italic; }}
        a {{ color: var(--main-blue); text-decoration: underline; font-weight: bold; }}
        a:hover {{ color: var(--alert-red); }}
        .modal {{ display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); }}
        .modal-content {{ background: #fff; margin: 15% auto; padding: 40px; width: 80%; max-width: 600px; border-radius: 8px; position: relative; }}
        .close {{ position: absolute; top: 10px; right: 20px; font-size: 30px; cursor: pointer; color: #333; }}
    </style></head>
    <body>
    <header><div class="brand">CAPITAL INSIGHT</div><div style="font-size:0.9rem; color:#ccc;">WARNING: SYSTEMIC RISK DETECTED</div></header>
    <div class="container">
        <main>
            <div style="background: #ffebee; color: #c62828; padding: 10px; font-weight: bold; display: inline-block; margin-bottom: 15px; border-radius: 4px;">⚠️ URGENT MARKET UPDATE</div>
            <h1>{topic}</h1><img src="{img_url}"><div class="content">{body_html}</div>
        </main>
        <aside class="sidebar">
            <div class="side-card">
                <div style="text-align:center; font-weight:bold; margin-bottom:15px; color:#d90429;">🔻 PROTECT YOUR WEALTH</div>
                <a href="{EMPIRE_URL}" class="btn">🚀 EXECUTE EXIT PLAN</a>
                <a href="{AFFILIATE_LINK}" class="btn" style="background: #001f3f;">📉 SHORT THE BANKS</a>
                <a href="{AMAZON_LINK}" class="btn" style="background: #f59f00; color:#000;">🛡️ BUY HARDWARE WALLET</a>
            </div>
            <div class="side-card">
                <h3 style="color:var(--main-blue); font-family:'Oswald'; border-bottom:2px solid #eee; padding-bottom:10px;">RECENT ALERTS</h3>
                <ul style="list-style:none; padding:0; font-size:0.9rem;">{sidebar_html}</ul>
            </div>
        </aside>
    </div>
    <footer>
        <div class="footer-links">
            <a onclick="openModal('about')">About</a>
            <a onclick="openModal('privacy')">Privacy</a>
            <a onclick="openModal('contact')">Contact</a>
        </div>
        &copy; 2026 {BLOG_TITLE}. <br>
        <span style="font-size:0.8rem;">Disclaimer: This content is for informational purposes only. Trading involves risk.</span>
        <div class="amazon-disclaimer">* As an Amazon Associate, we earn from qualifying purchases.</div>
    </footer>
    <div id="infoModal" class="modal"><div class="modal-content"><span class="close" onclick="closeModal()">&times;</span><div id="modalBody"></div></div></div>
    <script>
        const info = {{
            about: "<h2>About Capital Insight</h2><p>We provide unfiltered analysis of the global financial collapse and strategies for wealth preservation.</p>",
            privacy: "<h2>Privacy Policy</h2><p>We respect your privacy. Standard analytics cookies are used.</p>",
            contact: "<h2>Contact</h2><p>Email: admin@empire-analyst.digital</p>"
        }};
        function openModal(id) {{ document.getElementById('modalBody').innerHTML = info[id]; document.getElementById('infoModal').style.display = "block"; }}
        function closeModal() {{ document.getElementById('infoModal').style.display = "none"; }}
    </script>
    </body></html>"""

def main():
    topic = get_live_trends()[0] 
    body_text = generate_deep_report(topic) 
    html_body = markdown.markdown(body_text)
    # 이미지도 자극적이고 어두운 톤으로 변경
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('financial crisis panic wall street crash red charts dark cinematic 8k')}?width=1200&height=600"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = "".join([f"<li style='margin-bottom:10px;'>🚨 <a href='{BLOG_BASE_URL}{h.get('file','')}' style='color:#333; text-decoration:none;'>{h.get('title')[:25]}...</a></li>" for h in history[:10]])
    
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    generate_seo_files(history)
    
    full_html = create_final_html(topic, img_url, html_body, sidebar_html)
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)

if __name__ == "__main__": main()
