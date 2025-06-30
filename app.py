import streamlit as st
import re
import anthropic

# Claude API 키 설정 (본인 키로 교체하세요)
client = anthropic.Anthropic(
    api_key="your-claude-api-key-here"
)

# 페이지 설정
st.set_page_config(
    page_title="AI Script Extractor Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 프리미엄 CSS 스타일
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 3rem;
        margin: 2rem 0;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .header-container {
        text-align: center;
        margin-bottom: 3rem;
        position: relative;
    }
    
    .header-container::before {
        content: '';
        position: absolute;
        top: -20px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 2px;
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        line-height: 1.2;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #64748b;
        margin-top: 1rem;
        font-weight: 400;
        line-height: 1.6;
    }
    
    .feature-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.7) 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    .section-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 500;
        margin: 1rem 0;
    }
    
    .status-success {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
    }
    
    .status-error {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
    }
    
    .ai-processing {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 16px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        margin: 1.5rem 0;
    }
    
    .ai-processing h3 {
        color: #667eea;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .progress-bar {
        width: 100%;
        height: 8px;
        background: rgba(102, 126, 234, 0.2);
        border-radius: 4px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 4px;
        animation: progress 2s ease-in-out infinite;
    }
    
    @keyframes progress {
        0% { width: 0%; }
        50% { width: 70%; }
        100% { width: 100%; }
    }
    
    .result-container {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
        border-radius: 16px;
        padding: 2rem;
        border: 1px solid rgba(16, 185, 129, 0.2);
        margin: 1.5rem 0;
    }
    
    .chunk-container {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    }
    
    .chunk-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Streamlit 컴포넌트 스타일링 */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid rgba(102, 126, 234, 0.2) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        transition: all 0.3s ease !important;
        cursor: text !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    .stTextArea textarea:hover {
        border-color: rgba(102, 126, 234, 0.4) !important;
        cursor: text !important;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1) !important;
    }
    
    .floating-element {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 50%;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        font-size: 1.5rem;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

def extract_youtube_script(text):
    # 1. '동영상에서 검색' 이후 텍스트만 가져오기
    parts = re.split(r"동영상에서\s*검색", text, maxsplit=1)
    if len(parts) < 2:
        return None, "'동영상에서 검색' 키워드를 찾을 수 없습니다."
    after_search = parts[1]

    # 2. '모두' 나오기 전까지 자르기
    idx = after_search.find("모두")
    if idx != -1:
        after_search = after_search[:idx]

    # 3. 영어 문장만 필터링 (한글/한자 포함 문장 제외)
    lines = after_search.splitlines()
    english_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 영문자 포함, 한글/한자 미포함 문장만
        if re.search(r"[a-zA-Z]", line) and not re.search(r"[가-힣\u4e00-\u9fff]", line):
            english_lines.append(line)

    # 4. 결과 반환
    result = "\n".join(english_lines).strip()
    if not result:
        return None, "스크립트 내 영어 문장을 찾을 수 없습니다."
    return result, None

# 플로팅 엘리먼트
st.markdown('<div class="floating-element">🎯</div>', unsafe_allow_html=True)

# 메인 콘텐츠 영역
with st.container():
    st.markdown("""
    <div class="main-container">
        <div class="header-container">
            <h1 class="main-title">🎯 AI Script Extractor Pro</h1>
            <p class="subtitle">고급 AI 기술로 텍스트에서 스크립트를 추출하고 지능적으로 요약하는 프리미엄 솔루션</p>
        </div>
    """, unsafe_allow_html=True)

    # 입력 섹션
    st.markdown("""
    <div class="feature-card">
        <div class="section-title">📄 텍스트 입력</div>
        <p style="color: #64748b; margin-bottom: 1rem;">분석하고자 하는 전체 텍스트를 아래 영역에 입력해주세요.</p>
    """, unsafe_allow_html=True)
    
    user_text = st.text_area(
        "",
        placeholder="여기에 분석할 텍스트를 입력하세요... (스마트 분석 엔진이 자동으로 스크립트 부분을 감지합니다)",
        height=350,
        key="input_text"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)

    if user_text:
        # 통계 정보 표시
        word_count = len(user_text.split())
        char_count = len(user_text)
        
        st.markdown(f"""
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{char_count:,}</div>
                <div class="stat-label">총 문자 수</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{word_count:,}</div>
                <div class="stat-label">단어 수</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(user_text.splitlines())}</div>
                <div class="stat-label">라인 수</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        script_text, error = extract_youtube_script(user_text)
        
        if error:
            st.markdown(f"""
            <div class="status-badge status-warning">
                ⚠️ {error}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="status-badge status-success">
                ✅ 스크립트 추출 완료
            </div>
            """, unsafe_allow_html=True)
            
            # 분할 함수 정의
            def split_text(text):
                chunks = []
                start = 0
                length = len(text)
                while start < length:
                    segment = text[start:start+30000]
                    if re.search(r"[가-힣\u4e00-\u9fff\u3040-\u309F\u30A0-\u30FF]", segment):
                        segment = text[start:start+10000]
                    chunks.append(segment)
                    start += len(segment)
                return chunks

            chunks = split_text(script_text)

            # 추출 결과 섹션
            st.markdown("""
            <div class="feature-card">
                <div class="section-title">🎬 추출된 스크립트</div>
                <p style="color: #64748b; margin-bottom: 1.5rem;">AI가 식별한 스크립트 내용입니다.</p>
            """, unsafe_allow_html=True)

            # 분할된 텍스트 각각 출력
            for i, chunk in enumerate(chunks):
                st.markdown(f"""
                <div class="chunk-container">
                    <div class="chunk-title">📝 스크립트 부분 {i+1}/{len(chunks)}</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.text_area(
                    "",
                    value=chunk,
                    height=250,
                    key=f"chunk_{i}"
                )
            
            st.markdown("</div>", unsafe_allow_html=True)

            # AI 요약 버튼
            st.markdown("""
            <div class="feature-card" style="text-align: center;">
                <div class="section-title" style="justify-content: center;">🧠 AI 분석 및 요약</div>
                <p style="color: #64748b; margin-bottom: 2rem;">Claude AI의 고급 언어 모델을 활용하여 스크립트를 지능적으로 분석하고 요약합니다.</p>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 AI 요약 시작하기", key="summarize_btn"):
                st.markdown("""
                <div class="ai-processing">
                    <h3>🤖 Claude AI가 텍스트를 분석하고 있습니다...</h3>
                    <div class="progress-bar">
                        <div class="progress-fill"></div>
                    </div>
                    <p style="color: #64748b; margin: 0;">고급 자연어 처리 기술을 사용하여 정확한 요약을 생성하는 중입니다.</p>
                </div>
                """, unsafe_allow_html=True)
                
                try:
                    prompt = f"""다음 스크립트를 한국어로 간결하게 요약해주세요. \n\n스크립트:\n{script_text}\n\n요약:"""

                    message = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=800,
                        temperature=0.3,
                        messages=[{"role": "user", "content": prompt}]
                    )

                    summary = message.content[0].text.strip()
                    
                    st.markdown("""
                    <div class="result-container">
                        <div class="section-title">🎯 AI 요약 결과</div>
                        <div class="status-badge status-success">
                            ✅ 분석 완료
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.text_area(
                        "",
                        value=summary,
                        height=300,
                        key="summary_result"
                    )
                    
                    st.markdown("</div>", unsafe_allow_html=True)

                except Exception as e:
                    st.markdown(f"""
                    <div class="status-badge status-error">
                        ❌ 요약 중 오류가 발생했습니다: {str(e)}
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# 푸터
st.markdown("""
<div style="text-align: center; padding: 2rem; color: rgba(255, 255, 255, 0.7); font-size: 0.9rem;">
    <p>🎯 AI Script Extractor Pro | Powered by Claude AI & Advanced NLP Technology</p>
</div>
""", unsafe_allow_html=True)