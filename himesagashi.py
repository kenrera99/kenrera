import streamlit as st
import random
from PIL import Image

st.set_page_config(page_title="カップシャッフルゲーム", layout="centered")

st.title("カップシャッフルゲーム")

# 画像の読み込み
hime_img = st.file_uploader("姫の画像（hime.png）をアップロード", type=["png"], key="hime")
kerai_img = st.file_uploader("家来の画像（kerai.png）をアップロード", type=["png"], key="kerai")

if hime_img and kerai_img:
    hime = Image.open(hime_img).resize((60, 60))
    kerai = Image.open(kerai_img).resize((60, 60))
else:
    st.warning("姫と家来の画像をアップロードしてください。")
    st.stop()

# セッション状態の初期化
if "cup_map" not in st.session_state:
    hime_index = random.randint(0, 2)
    cup_map = ["kerai"] * 3
    cup_map[hime_index] = "hime"
    st.session_state.cup_map = cup_map
    st.session_state.shuffled = False
    st.session_state.selected = None
    st.session_state.result = ""
    st.session_state.shuffle_times = random.randint(5, 15)

# シャッフルボタン
if not st.session_state.shuffled:
    if st.button("カップをシャッフル！"):
        cup_map = st.session_state.cup_map
        for _ in range(st.session_state.shuffle_times):
            i, j = random.sample([0, 1, 2], 2)
            cup_map[i], cup_map[j] = cup_map[j], cup_map[i]
        st.session_state.cup_map = cup_map
        st.session_state.shuffled = True
        st.experimental_rerun()
    else:
        st.write("↓ シャッフルボタンを押してください")
        cols = st.columns(3)
        for i in range(3):
            with cols[i]:
                st.image(hime if st.session_state.cup_map[i] == "hime" else kerai, caption=f"カップ{i+1}")
        st.stop()

# カップ選択
st.write("どのカップに姫がいる？")
cols = st.columns(3)
for i in range(3):
    with cols[i]:
        if st.session_state.selected is None:
            if st.button(f"カップ{i+1}を選ぶ", key=f"select_{i}"):
                st.session_state.selected = i
                if st.session_state.cup_map[i] == "hime":
                    st.session_state.result = "正解！姫を見つけました！"
                else:
                    st.session_state.result = "残念、不正解…"
                st.experimental_rerun()
        else:
            # 結果表示
            st.image(hime if st.session_state.cup_map[i] == "hime" else kerai, caption=f"カップ{i+1}")

if st.session_state.selected is not None:
    st.subheader(st.session_state.result)
    if st.button("もう一度遊ぶ"):
        for key in ["cup_map", "shuffled", "selected", "result", "shuffle_times"]:
            if key in st.session_state:
                del st.session_state[key]
        st.experimental_rerun()