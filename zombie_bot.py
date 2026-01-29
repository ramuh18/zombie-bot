import os, json, random, requests, markdown, urllib.parse, feedparser, tweepy, time, re
from datetime import datetime

# ==========================================
# [기본 설정 및 로그]
# ==========================================
def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def get_env(key):
    val = os.environ.get(key, "")
    if not val or "***" in val: return ""
    return val.strip()

# 환경변수 및 링크 설정
AMAZON_TAG = "empireanalyst-20"
BYBIT_LINK = "https://www.bybit.com/invite?ref=DOVWK5A"
BLOG_BASE_URL = "https://ramuh18.github.io/zombie-bot/"
EMPIRE_URL = "https://empire-analyst.digital"

GEMINI_API_KEY = get_env("GEMINI_API_KEY")
DEVTO_TOKEN = get_env("DEVTO_TOKEN")
X_API_KEY = get_env("X_API_KEY")
X_API_SECRET = get_env("X_API_SECRET")
X_ACCESS_TOKEN = get_env("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = get_env("X_ACCESS_TOKEN_SECRET")

# ==========================================
# [1. 주제 선정 엔진]
# ==========================================
def get_hot_topic():
    topics = [
        "Bitcoin Supercycle 2026: Institutional Analysis",
        "Gold vs US Dollar: The Ultimate Hedge Strategy",
        "AI Tech Bubble: Risk Assessment & Outlook",
        "Global Liquidity Crisis: Crypto Market Impact",
        "Ethereum ETF Flows: On-Chain Data Review"
    ]
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        if feed.entries: return feed.entries[0].title
    except: pass
    return random.choice(topics)

# ==========================================
# [2. 텍스트 세척 엔진 (강력한 외계어 제거)]
# ==========================================
def clean_chunk(text):
    text = text.strip()
    
    # 1. JSON 정밀 타격 (사용자님 화면에 뜬 그 외계어 잡는 부분)
    # JSON처럼 생겼거나 'reasoning_content'라는 단어가 보이면 파싱 시도
    if text.startswith("{") or "reasoning_content" in text:
        try:
            # 특수문자 깨짐 방지 처리 후 파싱
            clean_json_text = text.replace('\n', '\\n').replace('\t', '\\t') 
            # 만약 파싱 가능한 JSON이면
            match = re.search(r'(\{.*\})', text, re.DOTALL)
            if match:
                data = json.loads(match.group(1))
                # 'content'가 진짜 본문입니다. reasoning_content는 버립니다.
                if 'content' in data and data['content']:
                    text = data['content']
                elif 'choices' in data:
                    text = data['choices'][0]['message']['content']
        except:
            # 파싱 실패하면 정규식으로 'content' 내용만 억지로 뜯어냄
            content_match = re.search(r'"content"\s*:\s*"(.*?)"', text, re.DOTALL)
            if content_match:
                text = content_match.group(1).replace('\\n', '\n').replace('\\"', '"')

    # 2. 잡설 및 광고 문구 제거
    patterns = [
        r"Powered by Pollinations.*", r"Running on free AI.*", 
        r"Here is the.*", r"Sure, I can.*", r"In this report.*",
        r"Image:.*", r"🌸 Ad 🌸.*",
        r'\{"role":.*?\}' # 혹시 남은 JSON 찌꺼기 제거
    ]
    for p in patterns:
        text = re.sub(p, "", text, flags=re.IGNORECASE)
    
    # 3. ★ 최후의 보루: '##'(제목) 앞부분은 무조건 잘라버림
    # 외계어가 아무리 길어도, 첫 번째 제목(##)이 나오기 전까진 다 쓰레기로 간주
    match = re.search(r'(##\s)', text)
    if match:
        text = text[match.start():]
    
    return text.strip()

# ==========================================
# [3. 콘텐츠 생성 엔진 (3단 합체 - 롱폼 전략)]
# ==========================================
def generate_part(topic, section_focus):
    """각 섹션별로 400단어 이상씩 쓰게 해서 이어 붙임"""
    prompt = f"""
    Act as a Senior Financial Analyst. Write a DETAILED section for a report on '{topic}'.
    Focus ONLY on: {section_focus}
    Length: Minimum 400 words. Deep dive.
    Format: Markdown (use ## for subheadings).
    IMPORTANT: OUTPUT ONLY THE ARTICLE TEXT. NO REASONING. NO JSON.
    """
    
    for attempt in range(2):
        try:
            # 1순위: Gemini
            if GEMINI_API_KEY:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
                resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=45)
                if resp.status_code == 200:
                    result = clean_chunk(resp.json()['candidates'][0]['content']['parts'][0]['text'])
                    if len(result) > 200: return result

            # 2순위: Pollinations
            url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
            resp = requests.get(url, timeout=60)
            result = clean_chunk(resp.text)
            if len(result) > 200: return result
            
        except: time.sleep(1)
    
    # 실패 시 비상용 문구 (JSON 노출 방지)
    return f"## Analysis Update\n\nData processing for {section_focus} encountered a format error. Retrying in next cycle."

def generate_full_report(topic):
    log(f"🧠 주제: {topic} (3단 합체 작성 시작)")
    
    # Part 1: 서론 & 거시경제
    log("✍️ Part 1 작성 중...")
    part1 = generate_part(topic, "Executive Summary, Macroeconomic Backdrop, Interest Rates, and Inflation Data.")
    
    # Part 2: 기관 & 기술적 분석
    log("✍️ Part 2 작성 중...")
    part2 = generate_part(topic, "Institutional Capital Flows, ETF Holdings, Smart Money positioning, and Technical Analysis.")
    
    # Part 3: 전망 & 전략
    log("✍️ Part 3 작성 중...")
    part3 = generate_part(topic, "Geopolitical Risks, Future Outlook, and Actionable Investment Strategy.")
    
    full_text = f"{part1}\n\n{part2}\n\n{part3}"
    log(f"✅ 리포트 완성 (총 길이: {len(full_text)}자)")
    return full_text

# ==========================================
# [4. 메인 실행 & 디자인 조립]
# ==========================================
def main():
    log("🏁 Empire Analyst (Anti-JSON Version) 가동")
    topic = get_hot_topic()
    
    # 글 생성 및 HTML 변환
    raw_md = generate_full_report(topic)
    
    # 혹시라도 전체 글이 JSON으로 시작하면 한 번 더 세척
    raw_md = clean_chunk(raw_md)
    
    html_content = markdown.markdown(raw_md)
    
    # 동적 요소
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(topic + ' chart 8k')}"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # [디자인] 1. 슬림 블랙 헤더
    header_section = f"""
    <div style="background: #000; color: white; padding: 20px 15px; text-align: center; border-radius: 0 0 15px 15px; margin-bottom: 30px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
        <div style="font-family: serif; font-size: 1.8rem; font-weight: 800; letter-spacing: 1px; line-height: 1;">EMPIRE ANALYST</div>
        <div style="font-size: 0.75rem; color: #f1c40f; margin-top: 5px; font-weight: bold; letter-spacing: 2px;">DEEP DIVE REPORT</div>
    </div>
    """

    # [디자인] 2. 광고 섹션 (바이비트/아마존 고정)
    ads_section = f"""
    <div style="margin: 40px 0; padding: 25px; background: #f8f9fa; border: 1px solid #ddd; border-radius: 10px; text-align: center;">
        <h3 style="margin-top: 0; font-size: 1.2rem; color: #333;">⚡ Strategic Allocation</h3>
        <div style="display: flex; flex-direction: column; gap: 10px; max-width: 350px; margin: 15px auto 0;">
            <a href="{BYBIT_LINK}" target="_blank" style="background: #000; color: #f1c40f; padding: 12px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 1rem;">🎁 Claim $30,000 Bonus</a>
            <a href="https://www.amazon.com/s?k=gold&tag={AMAZON_TAG}" target="_blank" style="background: #e67e22; color: white; padding: 12px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 1rem;">🛡️ Check Gold Prices</a>
        </div>
    </div>
    """

    # [디자인] 3. 푸터
    footer_section = f"""
    <div style="margin-top: 50px; padding: 30px 20px; background: #111; color: white; border-radius: 12px; text-align: center;">
        <h3 style="color: white; margin: 0 0 15px 0; font-size: 1.2rem;">Empire Analyst HQ</h3>
        <a href="{EMPIRE_URL}" style="display: inline-block; background: white; color: black; padding: 8px 20px; border-radius: 20px; font-weight: bold; text-decoration: none; font-size: 0.9rem;">Official Site →</a>
    </div>
    """

    # [디자인] 4. 전체 HTML 조립
    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{topic}</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.7; color: #333; max-width: 700px; margin: 0 auto; background-color: #fff; padding-bottom: 50px; }}
            img {{ width: 100%; height: auto; border-radius: 8px; margin: 20px 0; }}
            h1 {{ font-size: 1.8rem; margin: 10px 0 10px 0; padding: 0 15px; line-height: 1.3; }}
            .meta {{ font-size: 0.75rem; color: #aaa; padding: 0 15px; font-weight: bold; }}
            .content {{ padding: 0 15px; font-size: 1rem; text-align: justify; }}
            h2 {{ color: #2c3e50; font-size: 1.4rem; margin-top: 40px; border-bottom: 2px solid #f5f5f5; padding-bottom: 5px; }}
            li {{ margin-bottom: 8px; }}
            a {{ color: #2980b9; text-decoration: none; }}
        </style>
    </head>
    <body>
        {header_section}
        <div class="meta">UPDATED: {current_time}</div>
        <h1>{topic}</h1>
        <img src="{img_url}" alt="Chart">
        <div class="content">{html_content}</div>
        {ads_section}
        {footer_section}
    </body>
    </html>
    """

    # 파일 저장
    try:
        with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
        log("✅ index.html 파일 저장 완료")
    except Exception as e: log(f"❌ 저장 실패: {e}")

    # Dev.to 업로드
    if DEVTO_TOKEN:
        try: requests.post("https://dev.to/api/articles", headers={"api-key": DEVTO_TOKEN}, json={"article": {"title": topic, "published": True, "body_markdown": raw_md, "canonical_url": BLOG_BASE_URL}}, timeout=10)
        except: pass
    
    # X(트위터) 업로드
    if X_API_KEY:
        try:
            client = tweepy.Client(X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET)
            client.create_tweet(text=f"⚡ Report: {topic}\n\nLink: {BLOG_BASE_URL}")
        except: pass

if __name__ == "__main__":
    main()
