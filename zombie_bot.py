import os, json, random, requests, markdown, urllib.parse, feedparser, tweepy
from datetime import datetime
import time

# ==========================================
# [0. 안전 장치: 비밀번호 확인]
# ==========================================
def check_secrets():
    print("🔐 [시스템 점검] 비밀번호(Secrets) 확인 중...")
    keys = {
        "GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY"),
        "DEVTO_TOKEN": os.environ.get("DEVTO_TOKEN"),
        "X_API_KEY": os.environ.get("X_API_KEY")
    }
    for name, key in keys.items():
        if key:
            print(f"✅ {name}: 장착됨 (OK)")
        else:
            print(f"❌ {name}: 없음 (설정 필요!)")

# 기본 설정
AMAZON_TAG = "empireanalyst-20"
BYBIT_LINK = "https://www.bybit.com/invite?ref=DOVWK5A"
BLOG_BASE_URL = "https://zombie-bot.vercel.app"
EMPIRE_URL = "https://empire-analyst.digital"

# ==========================================
# [1. 백업 엔진 (무조건 긴 글)]
# ==========================================
def get_backup_article(topic, keyword):
    return f"""
### 🚨 Deep Dive Analysis: {topic}

**Executive Summary**
The markets are shifting correctly. Institutional order flow for **{keyword}** is hitting multi-year highs.

#### 1. Macro Outlook
Central banks are trapped. Liquidity is forced to enter the system, and **{keyword}** is the primary beneficiary. The risk-reward ratio at these levels is historically skewed in favor of bulls.

#### 2. On-Chain Data
Whales are not selling. Exchange reserves for **{keyword}** are plummeting, creating a supply shock.

#### 3. Strategic Plan
* **Buy**: Accumulate on dips.
* **Hold**: Use cold storage.
* **Trade**: Hedge on Bybit.

*Automated Analysis via Empire Analyst.*
    """

# ==========================================
# [2. 콘텐츠 생성 (에러 방지)]
# ==========================================
def generate_content_safe(topic, keyword):
    print("🧠 [AI] 글쓰기 시도 중...")
    
    # 1300자 요청 프롬프트
    prompt = f"Write a 1300-word financial report on '{topic}' and '{keyword}'. Markdown format. Professional tone."
    
    # 1차: 구글 Gemini
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            data = {"contents": [{"parts": [{"text": prompt}]}]}
            resp = requests.post(url, headers={'Content-Type': 'application/json'}, json=data, timeout=20)
            if resp.status_code == 200:
                text = resp.json().get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                if len(text) > 500: 
                    print("✅ Gemini 성공")
                    return text
        except Exception as e:
            print(f"⚠️ Gemini 에러: {e}")

    # 2차: 무료 AI
    try:
        simple_prompt = f"Write a long financial article about {keyword}"
        url = f"https://text.pollinations.ai/{urllib.parse.quote(simple_prompt)}"
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200 and len(resp.text) > 500:
            print("✅ 무료 AI 성공")
            return resp.text
    except Exception as e:
        print(f"⚠️ 무료 AI 에러: {e}")

    # 3차: 백업
    print("⚠️ 모든 AI 실패 -> 백업 원고 사용")
    return get_backup_article(topic, keyword)

# ==========================================
# [3. 업로드 함수 (절대 죽지 않음)]
# ==========================================
def post_to_devto_safe(title, md, canonical, img):
    token = os.environ.get("DEVTO_TOKEN")
    if not token:
        print("❌ Dev.to 업로드 불가: 토큰(DEVTO_TOKEN)이 없습니다.")
        return

    print(f"🚀 [Dev.to] 업로드 시도: {title}")
    try:
        data = {
            "article": {
                "title": title,
                "published": True,
                "body_markdown": md,
                "canonical_url": canonical,
                "cover_image": img,
                "tags": ["finance", "crypto", "investing"]
            }
        }
        resp = requests.post("https://dev.to/api/articles", 
                           headers={"api-key": token, "Content-Type": "application/json"}, 
                           json=data, timeout=15)
        if resp.status_code in [200, 201]:
            print(f"✅ [Dev.to] 성공! 주소: {resp.json()['url']}")
        else:
            print(f"❌ [Dev.to] 실패 (코드 {resp.status_code}): {resp.text}")
    except Exception as e:
        print(f"❌ [Dev.to] 치명적 에러: {e}")

def post_to_x_safe(text):
    print("🚀 [Twitter] 포스팅 시도...")
    try:
        client = tweepy.Client(
            consumer_key=os.environ.get("X_API_KEY"),
            consumer_secret=os.environ.get("X_API_SECRET"),
            access_token=os.environ.get("X_ACCESS_TOKEN"),
            access_token_secret=os.environ.get("X_ACCESS_TOKEN_SECRET")
        )
        resp = client.create_tweet(text=text)
        print(f"✅ [Twitter] 성공! ID: {resp.data['id']}")
    except Exception as e:
        print(f"❌ [Twitter] 실패: {e}")

# ==========================================
# [메인 실행]
# ==========================================
def main():
    print("🏁 좀비 봇 방탄 모드 시작")
    check_secrets() # 비밀번호 점검
    
    # 1. 뉴스 가져오기 (실패 시 기본값)
    hot_topic = "Global Market Shift"
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        if feed.entries:
            hot_topic = random.choice(feed.entries[:5]).title
            print(f"📰 뉴스 가져오기 성공: {hot_topic}")
    except Exception as e:
        print(f"⚠️ 뉴스 가져오기 실패: {e}")

    keyword = "Bitcoin" if "Crypto" in hot_topic else "Gold"
    
    # 2. 본문 생성
    raw_md = generate_content_safe(hot_topic, keyword)
    
    # 3. HTML 조립 및 저장 (★여기가 제일 중요★)
    # 이걸 try-except로 감싸서 무슨 일이 있어도 파일은 만들어지게 함
    try:
        image_prompt = urllib.parse.quote_plus(f"{hot_topic} {keyword} finance 8k")
        img_url = f"https://image.pollinations.ai/prompt/{image_prompt}"
        amz_link = f"https://www.amazon.com/s?k={keyword}&tag={AMAZON_TAG}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        promo = f"\n\n---\n### 🛡️ Asset: {keyword}\n[Check Price]({amz_link})\n### 💰 Bonus\n[$30k Bybit Bonus]({BYBIT_LINK})"
        final_content = f"![Header]({img_url})\n\n{raw_md}{promo}\n<small>Updated: {timestamp}</small>"
        
        html_body = markdown.markdown(final_content)
        full_html = f"<!DOCTYPE html><html><head><title>{hot_topic}</title><meta name='viewport' content='width=device-width, initial-scale=1'><style>body{{font-family:sans-serif;max-width:800px;margin:auto;padding:20px;line-height:1.6;}}img{{max-width:100%;border-radius:10px;}}a{{color:blue;font-weight:bold;}}</style></head><body><p>{timestamp}</p><h1>{hot_topic}</h1>{html_body}<a href='{EMPIRE_URL}' style='display:block;background:black;color:white;padding:15px;text-align:center;border-radius:5px;text-decoration:none;margin-top:30px;'>🚀 Empire Analyst Official</a></body></html>"
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        print("✅ index.html 파일 저장 완료 (Vercel 준비 끝)")
        
    except Exception as e:
        print(f"❌ 파일 저장 중 에러 발생: {e}")
        # 비상 파일이라도 저장
        with open("index.html", "w") as f: f.write("<h1>Emergency Mode</h1><p>Error occurred.</p>")

    # 4. 외부 업로드 (실패해도 스크립트 안 죽음)
    post_to_devto_safe(hot_topic, final_content, BLOG_BASE_URL, img_url)
    
    tweet_txt = f"⚡ {hot_topic}\n\nAnalyzing {keyword}.\n\nRead more: {BLOG_BASE_URL}\n\n#Finance #Crypto"
    post_to_x_safe(tweet_txt)
    
    print("🏁 모든 작업 완료")

if __name__ == "__main__":
    main()
