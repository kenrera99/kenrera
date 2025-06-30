import streamlit as st
import random

st.title("シャッフルゲーム")
st.write("3つのカップのどれかにボールが隠れています。シャッフル後、どこにあるか当ててみましょう！")

# 画像のパス
CUP_IMAGE = "cup.png"
BALL_IMAGE = "ball.png"

# セッション状態の初期化
if "cups" not in st.session_state:
    st.session_state.cups = [0, 0, 0]
    st.session_state.ball_pos = random.randint(0, 2)
    st.session_state.cups[st.session_state.ball_pos] = 1
    st.session_state.shuffled = False
    st.session_state.result = None

# シャッフルボタン
if st.button("カップをシャッフル！"):
    for _ in range(5):
        a, b = random.sample(range(3), 2)
        st.session_state.cups[a], st.session_state.cups[b] = st.session_state.cups[b], st.session_state.cups[a]
    st.session_state.shuffled = True
    st.session_state.result = None

# カップの表示
cols = st.columns(3)
for i in range(3):
    with cols[i]:
        st.image(CUP_IMAGE, width=120)
        if st.session_state.shuffled:
            if st.button(f"このカップを選ぶ", key=f"cup_{i}"):
                if st.session_state.cups[i] == 1:
                    st.session_state.result = "正解！おめでとうございます！"
                else:
                    st.session_state.result = f"残念！正解はカップ{st.session_state.cups.index(1)+1}でした。"

# 結果表示
if st.session_state.result:
    st.success(st.session_state.result)
    # 正解のカップの下にボール画像を表示
    cols[st.session_state.cups.index(1)].image(BALL_IMAGE, width=80)

# リセットボタン
if st.button("リセット"):
    st.session_state.cups = [0, 0, 0]
    st.session_state.ball_pos = random.randint(0, 2)
    st.session_state.cups[st.session_state.ball_pos] = 1
    st.session_state.shuffled = False
    st.session_state.result = None