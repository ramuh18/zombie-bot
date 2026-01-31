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

# [📊 실시간 트렌드 가져오기 함수]
def get_google_trends():
    try:
        # 미국 경제 트렌드 RSS (API 없이 접근 가능)
        url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
        resp = requests.get(url, timeout=20)
        titles = re.findall(r"<title>(.*?)</title>", resp.text)
        # 상위 1~2위는 무관할 수 있으므로 3~10위 사이에서 랜덤 선택
        if len(titles) > 5:
            return titles[3:10]
        return ["Global Market Reset", "Interest Rate Shift", "Digital Asset Surge"]
    except:
        return ["Economic Supercycle", "Inflationary Pressure", "Market Liquidity"]

# [🏛️ 1,500자급 하이브리드 원고 생성기]
def generate_trend_report(topic):
    # API가 될 때와 안 될 때를 모두 대비한 템플릿
    prompt = f"Write a 1500-word financial analysis about '{topic}'. Tone: Institutional. English Only. Markdown."
    
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.5, "maxOutputTokens": 1800}}, timeout=40)
        if resp.status_code == 200:
            return resp.json()['candidates'][0]['content']['parts'][0]['text'].strip()
    except:
        pass

    # [API 실패 시] 트렌드 키워드를 녹여낸 1,500자급 고정 리포트
    return f"""
# Strategic Analysis: The Impact of {topic} on 2026 Markets

The recent surge in interest regarding **{topic}** indicates a significant shift in market sentiment. Our strategic intelligence unit has monitored these developments closely to provide a comprehensive outlook.

## 1. Macro-Economic Context
The current trend of {topic} is not isolated. It follows a period of intense institutional accumulation and geopolitical realignment. As global liquidity tightens, assets related to {topic} are showing unprecedented volatility.

## 2. Institutional Response
Major hedge funds and sovereign wealth funds are repositioning their portfolios to account for the {topic} phenomenon. This move suggests that the underlying factors driving this trend are systemic rather than transitory.

## 3. Risk and Opportunity
For the retail investor, {topic} represents both a critical risk and a sovereign opportunity. Failure to secure one's assets in hardware-based storage could lead to significant capital erasure.

## 4. Final Conclusion
Monitoring {topic} is essential for the 2026 fiscal cycle. We recommend immediate migration to cold storage and the adoption of automated wealth preservation strategies.
    """

def create_final_html(topic, img_url, body_html, sidebar_html):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; background: #f4f7f9; color: #333; line-height: 1.8; margin: 0; }}
        header {{ background: #003366; color: white; padding: 25px; text-align: center; position: sticky; top:0; z-index:100; }}
        .container {{ max-width: 1200px; margin: 40px auto; display: grid; grid-template-columns: 1fr 320px; gap: 40px; padding: 0 20px; }}
        @media(max-width: 1000px) {{ .container {{ grid-template-columns: 1fr; }} .sidebar {{ position: static; }} }}
        main {{ background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        h1 {{ color: #003366; font-size: 2.8rem; line-height: 1.1; }}
        img {{ width: 100%; height: 450px; object-fit: cover; border-radius: 8px; margin-bottom: 30px; }}
        .sidebar {{ background: #fff; padding: 25px; border-radius: 8px; border-top: 4px solid #003366; }}
        .btn {{ display: block; padding: 15px; background: #003366; color: white; text-align: center; text-decoration: none; font-weight: bold; margin-top: 20px; }}
        footer {{ text-align: center; padding: 60px; color: #888; }}
    </style></head>
    <body>
    <header><h1>{BLOG_TITLE}</h1></header>
    <div class="container">
        <main><h1>{topic}</h1><img src="{img_url}"><div class="content">{body_html}</div></main>
        <aside class="sidebar"><h3>TRENDING NOW</h3><ul style="list-style:none; padding:0;">{sidebar_html}</ul><a href="{EMPIRE_URL}" class="btn">ACCESS FULL INTEL</a></aside>
    </div>
    <footer>&copy; 2026 {BLOG_TITLE}</footer></body></html>"""

def main():
    log("⚡ Trend-Tracking Update Initiated...")
    trends = get_google_trends()
    topic = random.choice(trends)
    
    full_text = generate_trend_report(topic)
    html_body = markdown.markdown(full_text)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('abstract financial data crystal red blue 8k')}"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = "".join([f"<li><a href='{BLOG_BASE_URL}{h.get('file','')}' style='color:#003366;'>{h.get('title')[:30]}...</a></li>" for h in history[:10]])
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_final_html(topic, img_url, html_body, sidebar_html)
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)
    log(f"✅ Trend Update Complete: {topic}")

if __name__ == "__main__": main()
