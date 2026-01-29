import os, json, random, requests, markdown, urllib.parse, feedparser, tweepy, time, re
from datetime import datetime

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [핵심 수정: 공백/줄바꿈 강력 제거]
def get_env(key):
    val = os.environ.get(key, "")
    if not val: return ""
    # 양쪽 공백 제거 + 중간에 낀 줄바꿈 문자 제거
    return val.strip().replace("\n", "").replace("\r", "")

AMAZON_TAG, BYBIT_LINK = "empireanalyst-20", "https://www.bybit.com/invite?ref=DOVWK5A"
BLOG_BASE_URL, EMPIRE_URL = "https://ramuh18.github.io/zombie-bot/", "https://empire-analyst.digital"
GEMINI_API_KEY, DEVTO_TOKEN = get_env("GEMINI_API_KEY"), get_env("DEVTO_TOKEN")
X_API_KEY, X_API_SECRET = get_env("X_API_KEY"), get_env("X_API_SECRET")
X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET = get_env("X_ACCESS_TOKEN"), get_env("X_ACCESS_TOKEN_SECRET")

def get_hot_topic():
    topics = ["Bitcoin Supercycle 2026", "Gold vs Dollar", "AI Tech Bubble Risks", "Global Liquidity Crisis"]
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        if feed.entries: return feed.entries[0].title
    except: pass
    return random.choice(topics)

def clean_chunk(text):
    text = text.strip()
    # 1. 외계어(JSON) 강제 해체
    if text.startswith("{") or "reasoning_content" in text:
        try:
            match = re.search(r'(\{.*\})', text, re.DOTALL)
            if match:
                data = json.loads(match.group(1))
                if 'content' in data: text = data['content']
                elif 'choices' in data: text = data['choices'][0]['message']['content']
        except:
            m = re.search(r'"content"\s*:\s*"(.*?)"', text, re.DOTALL)
            if m: text = m.group(1).replace('\\n', '\n').replace('\\"', '"')

    # 2. 잡설 제거
    patterns = [r"Powered by Pollinations.*", r"Running on free AI.*", r"Here is the.*", r"🌸 Ad 🌸.*", r'\{"role":.*?\}']
    for p in patterns: text = re.sub(p, "", text, flags=re.IGNORECASE)
    
    # 3. 제목(##) 앞부분 날리기
    match = re.search(r'(##\s)', text)
    if match: text = text[match.start():]
    return text.strip()

def generate_part(topic, focus):
    prompt = f"Act as a Senior Analyst. Write a DETAILED section on '{topic}'. Focus: {focus}. Length: 400+ words. Markdown. NO JSON."
    for _ in range(2):
        try:
            if GEMINI_API_KEY:
                url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY
                resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=45)
                if resp.status_code == 200: return clean_chunk(resp.json()['candidates'][0]['content']['parts'][0]['text'])
            url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
            resp = requests.get(url, timeout=60)
            return clean_chunk(resp.text)
        except: time.sleep(1)
    return f"## Update\nData for {focus} processing..."

def main():
    log("🏁 Empire Analyst (Crash-Proof Ver) 가동")
    topic = get_hot_topic()
    
    # 3단 합체 글쓰기
    p1 = generate_part(topic, "Executive Summary, Macro Backdrop")
    p2 = generate_part(topic, "Institutional Flows, Technical Analysis")
    p3 = generate_part(topic, "Risks, Outlook, Strategy")
    raw_md = clean_chunk(f"{p1}\n\n{p2}\n\n{p3}")
    html_body = markdown.markdown(raw_md)
    
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(topic + ' chart 8k')}"
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M UTC")

    full_html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{topic}</title>
    <style>body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;line-height:1.7;color:#333;max-width:700px;margin:0 auto;padding-bottom:50px}}img{{width:100%;border-radius:8px;margin:20px 0}}h1{{font-size:1.8rem;margin:10px 0;padding:0 15px}}h2{{color:#2c3e50;font-size:1.4rem;margin-top:40px;border-bottom:2px solid #f5f5f5}}.meta{{font-size:0.75rem;color:#aaa;padding:0 15px;font-weight:bold}}.content{{padding:0 15px;text-align:justify}}a{{color:#2980b9;text-decoration:none}}
    .header{{background:#000;color:#fff;padding:20px 15px;text-align:center;border-radius:0 0 15px 15px;margin-bottom:30px}}.ad-box{{margin:40px 0;padding:25px;background:#f8f9fa;border:1px solid #ddd;border-radius:10px;text-align:center}}.footer{{margin-top:50px;padding:30px 20px;background:#111;color:#fff;border-radius:12px;text-align:center}}
    </style></head><body>
    <div class="header"><div style="font-family:serif;font-size:1.8rem;font-weight:800">EMPIRE ANALYST</div><div style="font-size:0.75rem;color:#f1c40f;font-weight:bold">DEEP DIVE REPORT</div></div>
    <div class="meta">UPDATED: {time_str}</div><h1>{topic}</h1><img src="{img_url}"><div class="content">{html_body}</div>
    <div class="ad-box"><h3>⚡ Strategic Allocation</h3><div style="display:flex;flex-direction:column;gap:10px;max-width:350px;margin:15px auto"><a href="{BYBIT_LINK}" style="background:#000;color:#f1c40f;padding:12px;border-radius:6px;font-weight:bold;text-decoration:none">🎁 Claim $30,000 Bonus</a><a href="https://www.amazon.com/s?k=gold&tag={AMAZON_TAG}" style="background:#e67e22;color:#fff;padding:12px;border-radius:6px;font-weight:bold;text-decoration:none">🛡️ Check Gold Prices</a></div></div>
    <div class="footer"><h3>Empire Analyst HQ</h3><a href="{EMPIRE_URL}" style="background:#fff;color:#000;padding:8px 20px;border-radius:20px;font-weight:bold;text-decoration:none">Official Site →</a></div>
    </body></html>"""

    # 파일 저장 (이게 성공해야 사이트가 바뀜)
    try:
        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
        log("✅ index.html 저장 완료")
    except Exception as e: log(f"❌ 파일 저장 실패: {e}")

    # Dev.to 업로드 (안전 장치 추가)
    if DEVTO_TOKEN and len(DEVTO_TOKEN) > 10:
        try:
            log("🚀 Dev.to 업로드 시도...")
            requests.post("https://dev.to/api/articles", headers={"api-key": DEVTO_TOKEN}, json={"article": {"title": topic, "published": True, "body_markdown": raw_md, "canonical_url": BLOG_BASE_URL}}, timeout=10)
        except Exception as e: log(f"⚠️ Dev.to 업로드 실패 (무시하고 진행): {e}")

    # X 업로드 (안전 장치 추가)
    if X_API_KEY and len(X_API_KEY) > 10:
        try:
            log("🐦 X 업로드 시도...")
            tweepy.Client(X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET).create_tweet(text=f"⚡ Report: {topic}\n\nLink: {BLOG_BASE_URL}")
        except Exception as e: log(f"⚠️ X 업로드 실패 (무시하고 진행): {e}")

if __name__ == "__main__": main()
