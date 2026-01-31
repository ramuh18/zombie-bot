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
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = "https://www.amazon.com/s?k=ledger+nano+x&tag=empireanalyst-20"

# [주제 리스트: 50개]
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

# [핵심] 블록 15개 (내용 조립용)
CONTENT_BLOCKS = [
    """
    ## The Silent Wealth Transfer
    While the mainstream media distracts the public with trivial politics, a massive wealth transfer is occurring behind the scenes involving **{topic}**. Institutional whales are quietly accumulating assets while retail investors are being positioned to hold the bag. History shows that during every major cycle shift regarding {topic}, 90% of the population loses purchasing power, while the top 10% consolidate ownership. You must ask yourself: Which side of the trade are you on?
    """,
    """
    ## Historical Precedents and {topic}
    If we look back at the economic cycles of the 1970s and 2008, the patterns emerging with **{topic}** are terrifyingly similar. The debt-to-GDP ratios are unsustainable, and {topic} serves as the catalyst that could break the camel's back. The central banks have run out of ammunition. They cannot print their way out of the {topic} crisis without triggering hyperinflation. This is why smart money is exiting the fiat system rapidly.
    """,
    """
    ## Why Banks Don't Want You to Know About {topic}
    The legacy financial system relies on your ignorance about **{topic}**. As long as you keep your capital locked in depreciating savings accounts, they can leverage your money for their profit. However, {topic} represents a direct threat to their monopoly. By understanding the mechanics of {topic}, you can effectively 'opt-out' of their rigged game and reclaim your financial sovereignty.
    """,
    """
    ## The Mathematics of Collapse
    You don't need a PhD in economics to understand the math behind **{topic}**. It is a simple function of supply, demand, and liquidity. The current trajectory of {topic} suggests a mathematical inevitability of a system reset. When the derivatives market reacts to the volatility of {topic}, we could see a liquidity freeze that makes the 2008 crisis look like a minor correction.
    """,
    """
    ## Actionable Strategy: Surviving {topic}
    Hope is not a strategy. To survive the impact of **{topic}**, you need a concrete plan.
    1. **Audit your exposure:** How much of your net worth is tied to the success of the legacy system?
    2. **Hedge aggressively:** Use assets that inversely correlate with {topic}.
    3. **Self-Custody:** If you don't hold the keys, you don't own the chips.
    <div style="margin: 20px 0; padding: 15px; background: #ffebee; border-left: 5px solid #d90429;">
        <strong>🚨 CRITICAL ALERT:</strong> The window to secure your assets is closing. 
        <a href="{AMAZON_LINK}" style="color: #d90429; font-weight: bold;">[GET COLD STORAGE HARDWARE NOW]</a>
    </div>
    """,
    """
    ## The Institutional Trap
    Do not follow the herd. When JP Morgan and BlackRock talk about **{topic}** on TV, they are usually misleading the public to create liquidity for their own exits. The real moves regarding {topic} happen in the dark pools, away from retail eyes. Our analysis suggests they are shorting the very assets they tell you to buy. This is classic manipulation using {topic} as the narrative hook.
    """,
    """
    ## Technocratic Control and {topic}
    The push for **{topic}** is not accidental. It aligns perfectly with the agenda for greater centralized control over human activity. By controlling the narrative around {topic}, the powers that be can implement stricter capital controls and surveillance measures. Your only defense against this encroachment is decentralized assets and privacy-preserving technologies.
    """,
    """
    ## The 2026 Outlook for {topic}
    Looking ahead, the fiscal landscape for 2026 will be defined by how the world handles **{topic}**. We predict a bifurcation of the economy: those who hold hard assets and those who rely on government handouts. {topic} will be the dividing line. If you are not prepared for the volatility {topic} will bring, your portfolio could face a drawdown of 50% or more in real purchasing power terms.
    """,
    """
    ## The Currency Debasement Factor
    At the core of the **{topic}** issue lies the fundamental weakness of fiat currency. Since the decoupling from gold in 1971, the dollar has lost over 98% of its purchasing power. {topic} is merely the latest symptom of this terminal disease. Investors ignoring this reality are essentially storing their wealth in a melting ice cube.
    """,
    """
    ## Geopolitical Implications
    **{topic}** is not just an economic metric; it is a weapon of geopolitical warfare. Nations are actively positioning themselves around {topic} to gain leverage in the new multipolar world order. The BRICS alliance, in particular, is moving away from western financial hegemony, using {topic} as a wedge. This shift will catch most western investors completely off guard.
    """,
    """
    ## The Velocity of Money
    A critical, often overlooked aspect of **{topic}** is the velocity of money. As confidence in the system erodes, we expect a rapid increase in velocity, turning {topic} into a hyper-inflationary event. This is the "Crack-Up Boom" phase described by Austrian economists, where asset prices soar not because of value, but because the currency is dying.
    """,
    """
    ## Lessons from History
    Rome didn't fall in a day, but its currency did. The parallels between the late Roman Empire and today's indicators regarding **{topic}** are stark. Currency clipping then is quantitative easing now. The outcome is always the same: a wealth transfer from the poor to the asset-holding class. {topic} is your warning bell.
    """,
    """
    ## The Digital Panopticon
    While **{topic}** disrupts the market, it also paves the way for Central Bank Digital Currencies (CBDCs). The chaos caused by {topic} will be used as the justification for "safer" government-controlled digital money. This is the ultimate trap. Financial privacy will be a relic of the past unless you take steps to secure sovereign assets now.
    """,
    """
    ## Supply Chain Fragility
    The impact of **{topic}** extends into the physical world. Global supply chains, optimized for efficiency over resilience, are breaking under the strain of {topic}. We foresee shortages in critical commodities. This is not just about portfolio numbers; it's about access to essential resources.
    """,
    """
    ## The Final Exit Strategy
    How do you win against **{topic}**? You don't play their game. You exit. By moving capital into asymmetric bets—assets that have limited supply and high demand—you insulate yourself from the destruction caused by {topic}. This is the essence of the Empire Analyst strategy: profit from the collapse, don't be a victim of it.
    """
]

def get_live_trends():
    selected_topic = random.choice(BACKUP_TOPICS)
    return [selected_topic]

def generate_deep_report(topic):
    # 1. 인트로
    intro = f"""
# [URGENT_WARNING] The Truth About {topic} That They Won't Tell You

## Executive Summary
The global financial system is flashing red warning signals regarding **{topic}**. While the masses are asleep, a systemic shift is underway that will redefine wealth distribution for the next decade. This report exposes the harsh reality of {topic} and provides a roadmap for survival.
"""
    
    # 2. 본문 확장 (15개 중 5개 랜덤 조립)
    selected_blocks = random.sample(CONTENT_BLOCKS, 5)
    body_content = ""
    for block in selected_blocks:
        body_content += block.format(topic=topic, AMAZON_LINK=AMAZON_LINK) + "\n"

    # 3. 결론
    conclusion = f"""
## Final Verdict: The Time is Now
The timeline for **{topic}** is accelerating faster than anticipated. You can choose to ignore the warning signs, or you can take action today.
<br><br>
**Don't let your wealth evaporate.**
<div style="background: #f0f2f5; padding: 20px; text-align: center; border: 2px solid #001f3f; margin-top: 20px;">
    <h3>🚀 EXECUTE YOUR EXIT PLAN</h3>
    <p>The system is fragile. Secure your position before the liquidity dries up.</p>
    <a href="{EMPIRE_URL}" style="background: #d90429; color: white; padding: 15px 30px; text-decoration: none; font-weight: bold; border-radius: 5px; display: inline-block;">ACCESS FULL STRATEGY GUIDE</a>
    <br><br>
    <a href="{AFFILIATE_LINK}" style="color: #001f3f; font-weight: bold; text-decoration: underline;">>> Hedge with Derivatives on Bybit</a>
</div>
"""
    return intro + body_content + conclusion

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
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('financial crisis panic wall street crash red charts dark cinematic 8k')}?width=1200&height=600"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = "".join([f"<li style='margin-bottom:10px;'>🚨 <a href='{BLOG_BASE_URL}{h.get('file','')}' style='color:#333; text-decoration:none;'>{h.get('title')[:25]}...</a></li>" for h in history[:10]])
    
    # [수정 완료] 아래 라인이 에러가 났던 부분입니다. 확실히 고쳤습니다.
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    generate_seo_files(history)
    
    full_html = create_final_html(topic, img_url, html_body, sidebar_html)
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)

if __name__ == "__main__": main()
