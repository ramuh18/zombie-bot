import os, json, random, requests, markdown, urllib.parse, feedparser, tweepy
from datetime import datetime

# ==========================================
# [설정]
# ==========================================
AMAZON_TAG = "empireanalyst-20"
BYBIT_LINK = "https://www.bybit.com/invite?ref=DOVWK5A"
BLOG_BASE_URL = "https://zombie-bot.vercel.app"
EMPIRE_URL = "https://empire-analyst.digital"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DEVTO_TOKEN = os.environ.get("DEVTO_TOKEN")

# ==========================================
# [템플릿 엔진: AI가 죽었을 때 작동]
# ==========================================
def get_backup_article(topic, keyword):
    """AI 연결 실패 시 사용하는 고품질 비상용 원고"""
    return f"""
### 🚨 Critical Market Update: {topic}

The financial markets are signaling a major shift. Institutional investors are quietly accumulating positions in **{keyword}**, while retail investors are being shaken out.

#### Why {keyword}?
In times of volatility, smart money seeks safety and asymmetrical upside. **{keyword}** represents exactly that—a hedge against inflation and a vehicle for growth. The charts are showing a classic accumulation pattern.

#### The Institutional Trap
Most traders are looking at the wrong indicators. They are waiting for confirmation, but by the time the news is official, the move will be over. The volume profile on **{keyword}** suggests that a breakout is imminent.

#### Action Plan
1.  **Accumulate**: Dollar-cost average into positions.
2.  **Secure**: Do not leave assets on exchanges.
3.  **Leverage**: Use volatility to your advantage on platforms like Bybit.

*This analysis uses algorithmic trend following strategies.*
    """

# ==========================================
# [AI 엔진]
# ==========================================
def call_gemini(prompt):
    if not GEMINI_API_KEY: return None
    models = ["gemini-1.5-flash", "gemini-pro"]
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    for model in models:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
            resp = requests.post(url, headers=headers, json=data, timeout=10)
            if resp.status_code == 200:
                return resp.json()['candidates'][0]['content']['parts'][0]['text']
        except: continue
    return None

def call_pollinations_text(prompt):
    try:
        # 프롬프트가 너무 길면 실패할 수 있으니 단순화
        simple_prompt = f"Write a financial blog post about {prompt[:50]}..."
        url = f"https://text.pollinations.ai/{urllib.parse.quote(simple_prompt)}"
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200 and len(resp.text) > 100:
            return resp.text
    except: pass
    return None

def generate_content(topic, keyword):
    # 1. 메인 프롬프트
    prompt = f"Write a professional financial analysis on '{topic}' focusing on '{keyword}'. Tone: Urgent, Wall Street. Length: 800 words. Markdown."
    
    # AI 시도
    content = call_gemini(prompt)
    if content: return content
    
    content = call_pollinations_text(prompt)
    if content: return content
    
    # 전부 실패하면 템플릿 사용
    print("⚠️ AI 실패 -> 템플릿 엔진 가동")
    return get_backup_article(topic, keyword)

# ==========================================
# [메인 실행]
# ==========================================
def main():
    print("🚀 좀비 봇 가동 (Template Fallback Mode)")
    
    # 1. 주제 및 키워드
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        hot_topic = random.choice(feed.entries[:5]).title if feed.entries else "Global Wealth Shift"
    except: hot_topic = "Global Wealth Shift"
    
    # 키워드 추출 (단순화)
    product_keyword = "Gold" if "Gold" in hot_topic else "Bitcoin"
    if "Oil" in hot_topic: product_keyword = "Oil"
    if "Tech" in hot_topic: product_keyword = "Tech Stocks"
    
    print(f"📝 주제: {hot_topic} / 키워드: {product_keyword}")

    # 2. 본문 생성 (AI or 템플릿)
    raw_markdown = generate_content(hot_topic, product_keyword)

    # 3. 이미지 및 링크
    image_prompt = urllib.parse.quote_plus(f"{hot_topic} {product_keyword} cinematic 8k")
    header_image = f"https://image.pollinations.ai/prompt/{image_prompt}"
    
    amazon_link = f"https://www.amazon.com/s?k={urllib.parse.quote(product_keyword)}&tag={AMAZON_TAG}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 4. HTML 조립
    promo_md = f"""
    \n\n---
    ### 🏛️ Premium Research
    **[Read full analysis at Empire Analyst ->]({EMPIRE_URL})**
    
    ### 🛡️ Recommended Asset: {product_keyword}
    Check prices: **[Amazon Best Deals]({amazon_link})**
    \n
    ### 💰 Trade the News
    Get **$30,000 Bonus** on Bybit (`DOVWK5A`): **[Claim Bonus]({BYBIT_LINK})**
    """
    
    final_content = f"![Header]({header_image})\n\n" + raw_markdown + promo_md + f"\n\n<small>Updated: {timestamp}</small>"
    html_body = markdown.markdown(final_content)
    
    full_html = f"""
    <!DOCTYPE html>
    <html><head>
        <title>{hot_topic}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; line-height: 1.6; max-width: 800px; margin: auto; padding: 20px; color: #333; }}
            img {{ max-width: 100%; border-radius: 8px; margin: 20px 0; }}
            a {{ color: #d93025; font-weight: bold; text-decoration: none; }}
            h1 {{ font-size: 2.2em; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
            .btn {{ display: block; background: #000; color: #fff !important; text-align: center; padding: 15px; margin: 40px 0; border-radius: 5px; text-decoration: none; }}
        </style>
    </head>
    <body>
        <p style="color:#666; font-size:0.8em;">DAILY BRIEFING • {timestamp}</p>
        <h1>{hot_topic}</h1>
        {html_body}
        <a href="{EMPIRE_URL}" class="btn">🚀 Visit Official Empire Analyst Site</a>
    </body></html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    print("✅ index.html 생성 완료")
    
    post_to_devto(hot_topic, final_content, BLOG_BASE_URL, header_image)

if __name__ == "__main__": main()
