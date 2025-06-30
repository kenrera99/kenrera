import streamlit as st
import random

st.title("シャッフルゲーム")
st.write("3つのカップのどれかにボールが隠れています。シャッフル後、どこにあるか当ててみましょう！")

CUP_IMAGE = "cup.png"
BALL_IMAGE = "ball.png"

# セッション状態の初期化
if "cup_order" not in st.session_state:
    st.session_state.cup_order = [0, 1, 2]  # カップの並び順
    st.session_state.ball_pos = random.randint(0, 2)  # ボールの位置（カップ番号）
    st.session_state.shuffle_steps = []  # シャッフル手順
    st.session_state.current_step = 0
    st.session_state.shuffled = False
    st.session_state.result = None

# シャッフル手順を作成
def make_shuffle_steps(n=5):
    steps = []
    for _ in range(n):
        a, b = random.sample([0, 1, 2], 2)
        steps.append((a, b))
    return steps

# シャッフルボタン
if st.button("カップをシャッフル！"):
    st.session_state.cup_order = [0, 1, 2]
    st.session_state.ball_pos = random.randint(0, 2)
    st.session_state.shuffle_steps = make_shuffle_steps(5)
    st.session_state.current_step = 0
    st.session_state.shuffled = False
    st.session_state.result = None

# シャッフル動作を1手ずつ進める
if st.session_state.shuffle_steps and st.session_state.current_step < len(st.session_state.shuffle_steps):
    if st.button("次の動作を見る"):
        a, b = st.session_state.shuffle_steps[st.session_state.current_step]
        # 並び順を入れ替え
        st.session_state.cup_order[a], st.session_state.cup_order[b] = st.session_state.cup_order[b], st.session_state.cup_order[a]
        # ボールの位置も追従
        if st.session_state.ball_pos == a:
            st.session_state.ball_pos = b
        elif st.session_state.ball_pos == b:
            st.session_state.ball_pos = a
        st.session_state.current_step += 1
        # 全ての動作が終わったらシャッフル完了
        if st.session_state.current_step == len(st.session_state.shuffle_steps):
            st.session_state.shuffled = True

# カップの表示
cols = st.columns(3)
for idx, cup in enumerate(st.session_state.cup_order):
    with cols[idx]:
        st.image(CUP_IMAGE, width=120)
        st.markdown(f"**カップ{idx+1}**")
        if st.session_state.shuffled:
            disabled = st.session_state.result is not None
            if st.button(f"このカップを選ぶ", key=f"cup_{idx}", disabled=disabled):
                if idx == st.session_state.ball_pos:
                    st.session_state.result = "正解！おめでとうございます！"
                else:
                    st.session_state.result = f"残念！正解はカップ{st.session_state.ball_pos+1}でした。"

# 結果表示
if st.session_state.result:
    st.success(st.session_state.result)
    # 正解のカップの下にボール画像を表示
    cols[st.session_state.ball_pos].image(BALL_IMAGE, width=80)

# リセットボタン
if st.button("リセット"):
    st.session_state.cup_order = [0, 1, 2]
    st.session_state.ball_pos = random.randint(0, 2)
    st.session_state.shuffle_steps = []
    st.session_state.current_step = 0
    st.session_state.shuffled = False
    st.session_state.result = None