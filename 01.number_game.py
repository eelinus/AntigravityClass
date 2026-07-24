import random
import streamlit as st

# 페이지 설정을 적용합니다.
st.set_page_config(
    page_title="숫자 맞추기 게임",
    page_icon="🎯",
    layout="centered"
)

# 세션 상태(Session State) 초기화
if "target_number" not in st.session_state:
    st.session_state.target_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.history = []


def reset_game():
    st.session_state.target_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.history = []


# UI 타이틀 및 설명
st.title("🎯 숫자 맞추기 게임")
st.caption("Streamlit 기반 웹 애플리케이션")

st.markdown("""
---
### 📜 게임 규칙
1. 컴퓨터가 **1부터 100 사이**의 숫자를 무작위로 선택했습니다.
2. 아래 입력창에 숫자를 입력하고 **'추측하기'** 버튼을 눌러보세요.
3. **UP / DOWN** 힌트를 활용해 최소한의 시도 횟수로 정답을 맞춰보세요!
---
""")

# 상태 표시 메트릭
col1, col2 = st.columns(2)
with col1:
    st.metric(label="현재 시도 횟수", value=f"{st.session_state.attempts} 회")
with col2:
    status_text = "🎮 게임 진행 중" if not st.session_state.game_over else "🎉 정답 달성!"
    st.metric(label="게임 상태", value=status_text)

# 입력 폼
with st.form(key="guess_form", clear_on_submit=True):
    guess_input = st.number_input(
        "1~100 사이의 숫자를 입력하세요:",
        min_value=1,
        max_value=100,
        step=1,
        disabled=st.session_state.game_over,
        key="num_input"
    )
    submit_button = st.form_submit_button(
        label="🎲 추측하기",
        disabled=st.session_state.game_over
    )

# 버튼 클릭 시 처리
if submit_button and not st.session_state.game_over:
    st.session_state.attempts += 1
    guess = int(guess_input)

    if guess < st.session_state.target_number:
        st.session_state.history.append((guess, "UP 📈"))
    elif guess > st.session_state.target_number:
        st.session_state.history.append((guess, "DOWN 📉"))
    else:
        st.session_state.game_over = True
        st.session_state.history.append((guess, "정답! 🎉"))

# 결과 및 메시지 출력
if st.session_state.history:
    last_guess, last_result = st.session_state.history[-1]
    if last_result == "UP 📈":
        st.warning(f"📈 **UP!** `{last_guess}`보다 더 큰 숫자입니다.")
    elif last_result == "DOWN 📉":
        st.warning(f"📉 **DOWN!** `{last_guess}`보다 더 작은 숫자입니다.")
    elif st.session_state.game_over:
        st.success(f"🎉 **축하합니다!** 정답은 **{st.session_state.target_number}**이었습니다!")
        st.balloons()

        attempts = st.session_state.attempts
        if attempts <= 3:
            st.info("🏆 **신의 영역!** 아주 뛰어난 직관력이네요!")
        elif attempts <= 7:
            st.info("👏 **대단합니다!** 매우 우수한 성적입니다.")
        else:
            st.info("👍 **끝까지 포기하지 않고 정답을 맞추셨군요!**")

# 다시 시작 버튼
st.write("")
if st.button("🔄 새 게임 시작하기", type="primary"):
    reset_game()
    st.rerun()

# 추측 히스토리 표시
if st.session_state.history:
    st.divider()
    st.markdown("### 📊 시도 히스토리")
    for idx, (num, res) in enumerate(reversed(st.session_state.history)):
        turn_num = len(st.session_state.history) - idx
        st.write(f"**{turn_num}회차:** `{num}` ➔ **{res}**")
