import random
import time


def shuffle_cups(cups, shuffle_count=5):
    for _ in range(shuffle_count):
        idx1, idx2 = random.sample(range(3), 2)
        cups[idx1], cups[idx2] = cups[idx2], cups[idx1]
        print(f"カップ{idx1 + 1}とカップ{idx2 + 1}を入れ替えました。")
        time.sleep(0.7)
    return cups


def main():
    print("シャッフルゲームへようこそ！")
    print("1つのボールを3つのカップのどれかに隠します。")
    print("カップの位置をシャッフルしますので、どこにボールがあるか当ててください。")
    input("Enterキーで開始します...")

    # カップの初期化（0:空, 1:ボール）
    cups = [0, 0, 0]
    ball_position = random.randint(0, 2)
    cups[ball_position] = 1

    print("\nカップをシャッフルします...\n")
    cups = shuffle_cups(cups, shuffle_count=7)

    print("\nシャッフルが終わりました。")
    guess = int(input("ボールが入っているカップの番号を1, 2, 3から選んでください: ")) - 1

    if cups[guess] == 1:
        print("正解！おめでとうございます！")
    else:
        print("残念！ハズレです。")
        print(f"正解はカップ{cups.index(1) + 1}でした。")


if __name__ == "__main__":
    main()


# これはサンプルの Python スクリプトです。

# Ctrl+F5 を押して実行するか、ご自身のコードに置き換えてください。
# Shift を2回押す を押すと、クラス/ファイル/ツールウィンドウ/アクション/設定を検索します。


def print_hi(name):
    # スクリプトをデバッグするには以下のコード行でブレークポイントを使用してください。
    print(f'Hi, {name}')  # F9を押すとブレークポイントを切り替えます。


# ガター内の緑色のボタンを押すとスクリプトを実行します。
if __name__ == '__main__':
    print_hi('PyCharm')

# PyCharm のヘルプは https://www.jetbrains.com/help/pycharm/ を参照してください
