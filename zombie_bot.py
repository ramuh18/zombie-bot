import os, sys, datetime

# [진단 로그 기록 시작]
log = []
def add_log(msg):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {msg}")
    log.append(f"[{timestamp}] {msg}")

add_log("🚀 봇 시동 켜짐 (진단 모드 v2)")

# 1. 라이브러리 검사
try:
    import json, random, requests, markdown, urllib.parse, feedparser, tweepy
    add_log("✅ 필수 라이브러리 장착 완료")
except ImportError as e:
    add_log(f"❌ 라이브러리 누락 발생: {e}")
    add_log("⚠️ 해결책: Daily_run.yml 파일에서 pip install 명령어를 확인하세요.")

# 2. 비밀번호(Secrets) 검사
secrets = {
    "GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY"),
    "DEVTO_TOKEN": os.environ.get("DEVTO_TOKEN"),
    "X_API_KEY": os.environ.get("X_API_KEY")
}
for name, val in secrets.items():
    if val: add_log(f"✅ {name}: 연결됨")
    else: add_log(f"❌ {name}: 없음 (GitHub Settings 확인 필요!)")

# 3. 콘텐츠 생성 시도
add_log("🧠 콘텐츠 생성 시작...")
content = ""
hot_topic = "System Check"
try:
    # 뉴스 가져오기
    feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
    if feed.entries:
        hot_topic = feed.entries[0].title
        add_log(f"📰 뉴스 수신 성공: {hot_topic}")
    
    # 1300자 백업 원고 (AI 실패시 사용)
    content = f"""
    ### 🚨 Deep Dive Analysis: {hot_topic}
    **Executive Summary**
    The markets are shifting. Institutional order flow is hitting multi-year highs.
    (This is a backup generated text to ensure the site never stays empty.)
    """
    
    # AI 호출 (Gemini)
    if secrets["GEMINI_API_KEY"]:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={secrets['GEMINI_API_KEY']}"
            resp = requests.post(url, headers={'Content-Type': 'application/json'}, json={"contents": [{"parts": [{"text": f"Write a 1300 word financial article about {hot_topic}"}]}]}, timeout=10)
            if resp.status_code == 200:
                content = resp.json()['candidates'][0]['content']['parts'][0]['text']
                add_log("✅ Gemini AI 글쓰기 성공")
        except Exception as e:
            add_log(f"⚠️ Gemini 실패 (백업 사용): {e}")
except Exception as e:
    add_log(f"❌ 콘텐츠 생성 중 치명적 에러: {e}")

# 4. Dev.to 업로드 시도 (여기가 문제였음 - 수정완료)
if secrets["DEVTO_TOKEN"]:
    add_log("🚀 Dev.to 업로드 시도...")
    try:
        data = {
            "article": {
                "title": hot_topic,
                "published": True,
                "body_markdown": content,
                "tags": ["finance", "test"]
            }
        }
        resp = requests.post("https://dev.to/api/articles", 
                           headers={"api-key": secrets["DEVTO_TOKEN"], "Content-Type": "application/json"}, 
                           json=data, timeout=10)
        if resp.status_code == 201: add_log(f"✅ Dev.to 업로드 성공: {resp.json()['url']}")
        else: add_log(f"❌ Dev.to 실패 (코드 {resp.status_code}): {resp.text}")
    except Exception as e:
        add_log(f"❌ Dev.to 업로드 에러: {e}")
else:
    add_log("⚠️ DEVTO_TOKEN 없음: 업로드 건너뜀")

# 5. 결과 파일(index.html) 생성 - 무조건 실행됨
try:
    log_html = "<br>".join(log)
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{hot_topic}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: sans-serif; max-width: 800px; margin: auto; padding: 20px; }}
            .log {{ background: #eee; padding: 15px; border-radius: 5px; font-family: monospace; color: #333; }}
            .success {{ color: green; }} .error {{ color: red; }}
        </style>
    </head>
    <body>
        <h1>{hot_topic}</h1>
        <p>Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        <hr>
        {markdown.markdown(content)}
        <br><br>
        <h2>🛠️ 시스템 진단 리포트 (Debug Log)</h2>
        <div class="log">
            {log_html.replace('✅', '<span class="success">✅</span>').replace('❌', '<span class="error">❌</span>')}
        </div>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    add_log("✅ index.html 파일 생성 완료")
except Exception as e:
    print(f"FATAL ERROR: {e}")

print("🏁 진단 종료")
