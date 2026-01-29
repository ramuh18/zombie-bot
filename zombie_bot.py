import os, json, random, requests, markdown, urllib.parse, feedparser, tweepy, time, re
from datetime import datetime

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [설정]
AMAZON_TAG = "empireanalyst-20"
BYBIT_LINK = "https://www.bybit.com/invite?ref=DOVWK5A"
BLOG_BASE_URL = "https://ramuh18.github.io/zombie-bot/"
EMPIRE_URL = "https://empire-analyst.digital"

def get_env(key):
    val = os.environ.get(key, "")
    if not val: return ""
    return val.strip().replace("\n", "").replace("\r", "")

GEMINI_API_KEY, DEVTO_TOKEN = get_env("GEMINI_API_KEY"), get_env("DEVTO_TOKEN")
X_API_KEY, X_API_SECRET = get_env("X_API_KEY"), get_env("X_API_SECRET")
X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET = get_env("X_ACCESS_TOKEN"), get_env("X_ACCESS_TOKEN_SECRET")

# ==========================================
# [1. 텍스트 세척]
# ==========================================
def clean_text(text):
    text = text.strip()
    if text.startswith("{") or "reasoning_content" in text:
        try:
            m = re.search(r'(\{.*\})', text, re.DOTALL)
            if m:
                d = json.loads(m.group(1))
                if 'content' in d: text = d['content']
                elif 'choices' in d: text = d['choices'][0]['message']['content']
        except:
            m = re.search(r'"content"\s*:\s*"(.*?)"', text, re.DOTALL)
            if m: text = m.group(1).replace('\\n', '\n').replace('\\"', '"')
    
    patterns = [r"Powered by Pollinations.*", r"Running on free AI.*", r"Here is.*", r"Sure,.*", r"Title:", r"Headline:", r"\"", r"\*"]
    for p in patterns: text = re.sub(p, "", text, flags=re.IGNORECASE)
    return text.strip()

# ==========================================
# [2. 주제 선정 - 실시간 트렌드 + AI 후킹]
# ==========================================
def get_hot_topic():
    # 1. 구글 뉴스(Business)에서 실시간 트렌드 긁어오기
    raw_news = []
    try:
        # 미국 비즈니스 뉴스 RSS
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        if feed.entries:
            # 상위 5개 뉴스 중 하나 랜덤 선택 (매번 같은 글 방지)
            entries = feed.entries[:5]
            target_news = random.choice(entries).title
            log(f"📰 수집된 실시간 뉴스: {target_news}")
        else:
            target_news = "Global Market Volatility & Bitcoin"
    except:
        target_news = "Inflation & Tech Stock Crash"

    # 2. AI에게 '뉴스 제목'을 '클릭베이트'로 변환 요청
    prompt = f"""
    Rewrite this news headline into a SHOCKING, CLICKBAIT style.
    Original News: "{target_news}"
    
    Rules:
    1. Do NOT force the year 2026 (unless it's in the news).
    2. Use urgent words: ALERT, CRASH, EXPLOSION, WARNING, BREAKING.
    3. Keep it under 15 words.
    4. Make it sound like a financial emergency or huge opportunity.
    5. No quotes.
    """
    
    for _ in range(2):
        try:
            if GEMINI_API_KEY:
                url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY
                resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=15)
                if resp.status_code == 200:
                    title = clean_text(resp.json()['candidates'][0]['content']['parts'][0]['text'])
                    return title if len(title) > 5 else target_news
            
            # Pollinations 백업
            url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
            resp = requests.get(url, timeout=30)
            title = clean_text(resp.text)
            return title if len(title) > 5 else target_news
            
        except: time.sleep(1)
    
    return f"MARKET ALERT: {target_news}"

# ==========================================
# [3. 본문 생성]
# ==========================================
def generate_part(topic, focus):
    prompt = f"Act as a controversial financial analyst. Write a SHOCKING & DETAILED section on '{topic}'. Focus: {focus}. Length: 400+ words. Markdown. NO JSON. Use strong language."
    for _ in range(2):
        try:
            if GEMINI_API_KEY:
                url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY
                resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=45)
                if resp.status_code == 200: return clean_text(resp.json()['candidates'][0]['content']['parts'][0]['text'])
            url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
            resp = requests.get(url, timeout=60)
            return clean_text(resp.text)
        except: time.sleep(1)
    return f"## Update\nData processing for {focus}..."

# ==========================================
# [4. 히스토리 & 링크 관리]
# ==========================================
HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f: return json.load(f)
        except: pass
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f: json.dump(history, f, indent=4)

def get_internal_links_html(history, current_title):
    if len(history) < 2: return ""
    candidates = [h for h in history if h['title'] != current_title]
    if not candidates: return ""
    picks = random.sample(candidates, min(3, len(candidates)))
    
    links_html = """
    <div style="margin: 40px 0; padding: 20px; background: #fff3cd; border-left: 5px solid #d35400; border-radius: 5px;">
        <h3 style="margin-top: 0; font-size: 1.2rem; color: #d35400;">🔥 Trending Now</h3>
        <ul style="list-style: none; padding: 0;">
    """
    for p in picks:
        url = p.get('file', 'index.html') 
        links_html += f"<li style='margin-bottom: 10px;'><a href='{url}' style='text-decoration: none; color: #d35400; font-weight: bold;'>👉 {p['title']}</a></li>"
    links_html += "</ul></div>"
    return links_html

# ==========================================
# [5. 메인 실행]
# ==========================================
def main():
    log("🏁 Empire Analyst (Real-Time Trend Ver) 가동")
    
    # 1. 실시간 뉴스 기반 제목 생성
    topic = get_hot_topic()
    log(f"🔥 확정된 제목: {topic}")
    
    # 2. 3단 합체 본문 생성
    p1 = generate_part(topic, "Shocking Executive Summary & Macro Warning")
    p2 = generate_part(topic, "Whale Movements & Technical Collapse Signals")
    p3 = generate_part(topic, "Final Prediction & Survival Strategy")
    raw_md = clean_text(f"{p1}\n\n{p2}\n\n{p3}")
    html_body = markdown.markdown(raw_md)
    
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(topic + ' chart 8k')}"
    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    file_timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    archive_filename = f"post_{file_timestamp}.html"
    
    # 3. 히스토리 저장
    history = load_history()
    internal_links_box = get_internal_links_html(history, topic)
    new_entry = {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_filename}
    history.insert(0, new_entry)
    save_history(history)

    # 4. 아카이브 목록 HTML
    archive_list_html = "<ul style='list-style:none; padding:0;'>"
    for item in history[:15]:
        archive_list_html += f"<li style='margin-bottom:8px; border-bottom:1px solid #eee;'><a href='{item['file']}' style='text-decoration:none; color:#333; font-size:0.9rem;'>{item['title']}</a></li>"
    archive_list_html += "</ul>"

    # 5. HTML 조립
    def create_html(is_main_page):
        can_url = BLOG_BASE_URL if is_main_page else f"{BLOG_BASE_URL}{archive_filename}"
        return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{topic}</title>
        <link rel="canonical" href="{can_url}" />
        <style>body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;line-height:1.7;color:#333;max-width:700px;margin:0 auto;padding-bottom:50px}}img{{width:100%;border-radius:8px;margin:20px 0}}h1{{font-size:1.8rem;margin:10px 0;padding:0 15px;color:#c0392b}}h2{{color:#2c3e50;font-size:1.4rem;margin-top:40px;border-bottom:2px solid #f5f5f5}}.meta{{font-size:0.75rem;color:#aaa;padding:0 15px;font-weight:bold}}.content{{padding:0 15px;text-align:justify}}a{{color:#2980b9;text-decoration:none}}
        .header{{background:#000;color:#fff;padding:20px 15px;text-align:center;border-radius:0 0 15px 15px;margin-bottom:30px}}.ad-box{{margin:40px 0;padding:25px;background:#f8f9fa;border:1px solid #ddd;border-radius:10px;text-align:center}}.footer{{margin-top:50px;padding:30px 20px;background:#111;color:#fff;border-radius:12px;text-align:center}}
        .archive-box{{margin-top:50px;padding:20px;background:#fff;border-top:4px solid #000}}
        </style></head><body>
        <div class="header"><div style="font-family:serif;font-size:1.8rem;font-weight:800">EMPIRE ANALYST</div><div style="font-size:0.75rem;color:#f1c40f;font-weight:bold">DEEP DIVE REPORT</div></div>
        <div class="meta">UPDATED: {current_time_str}</div><h1>{topic}</h1><img src="{img_url}"><div class="content">{html_body}</div>
        {internal_links_box}
        <div class="ad-box"><h3>⚡ Strategic Allocation</h3><div style="display:flex;flex-direction:column;gap:10px;max-width:350px;margin:15px auto"><a href="{BYBIT_LINK}" style="background:#000;color:#f1c40f;padding:12px;border-radius:6px;font-weight:bold;text-decoration:none">🎁 Claim $30,000 Bonus</a><a href="https://www.amazon.com/s?k=gold&tag={AMAZON_TAG}" style="background:#e67e22;color:#fff;padding:12px;border-radius:6px;font-weight:bold;text-decoration:none">🛡️ Check Gold Prices</a></div></div>
        <div class="archive-box"><h3 style="color:#000;">📂 Recent Bombshells</h3>{archive_list_html}</div>
        <div class="footer"><h3>Empire Analyst HQ</h3><a href="{EMPIRE_URL}" style="background:#fff;color:#000;padding:8px 20px;border-radius:20px;font-weight:bold;text-decoration:none">Official Site →</a></div>
        </body></html>"""

    # 6. 파일 저장
    with open("index.html", "w", encoding="utf-8") as f: f.write(create_html(True))
    with open(archive_filename, "w", encoding="utf-8") as f: f.write(create_html(False))
    log(f"✅ 블로그 저장 완료: {archive_filename}")

    # 7. Dev.to 업로드
    if DEVTO_TOKEN:
        log("🚀 Dev.to 업로드 시도...")
        try:
            full_md = f"# {topic}\n\n{raw_md}\n\n## 🔗 Related Reports\nCheck out our previous analysis here: {BLOG_BASE_URL}"
            resp = requests.post("https://dev.to/api/articles", headers={"api-key": DEVTO_TOKEN}, json={"article": {"title": topic, "published": True, "body_markdown": full_md, "canonical_url": f"{BLOG_BASE_URL}{archive_filename}", "tags": ["finance", "crypto", "bitcoin", "investing"]}}, timeout=15)
            if resp.status_code not in [200, 201]: log(f"❌ Dev.to 실패: {resp.status_code} {resp.text}")
            else: log("✅ Dev.to 성공!")
        except Exception as e: log(f"⚠️ Dev.to 에러: {e}")

    # 8. X 업로드
    if X_API_KEY and len(X_API_KEY) > 10:
        try:
            tweepy.Client(X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET).create_tweet(text=f"🚨 ALERT: {topic}\n\nRead: {BLOG_BASE_URL}{archive_filename}")
        except: pass

if __name__ == "__main__": main()
