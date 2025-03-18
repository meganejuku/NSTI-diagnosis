import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np

# 診断タイトル変更
st.title("NSTI診断")
st.write("以下の質問に答えてください（7段階評価）")

# 各属性の質問リスト
questions_dict = {
    "S-N": [
        "大人数の前だとやる気が出てくる",
        "一人よりは二人、多ければ多いほどよい",
        "みんなに注目されると気持ちが良い",
        "一人は怖いものだ",
        "他人は利用してなんぼだと思う",
        "人を蹴落とすと気持ちが良い、たくさんやるべき",
        "宇宙人はいると思う",
        "世界中の人間を偉い順に並べると、自分は上位である"
    ],
    "A-Y": [
        "人生は、冒険だ",
        "自分の未来は明るいと感じる",
        "話しかけられるより、話しかける方が好きだ",
        "周りの人に「もっと効率的に動けばいいのに」とよく思う",
        "殺されるくらいなら、殺す",
        "物事に出遅れることはあまりない",
        "自分は流行に敏感だと感じる"
    ],
    "E-O": [
        "悲しくて泣いてしまうことはあまりない",
        "お酒が好きだ",
        "財布を落としても慌てずに行動できる自信がある",
        "クレジットカードが好きだ",
        "自分ならば、大抵のことは何とかなると思う",
        "正直に言うと、賢いという自負がある",
        "やるべきことをやる前でも遊べるタイプだ"
    ],
    "T-M": [
        "「どうしても」というなら、法律は破っても良いと思う",
        "マジックが好きだ",
        "引っ掛け問題に引っかからない自信がある",
        "「生まれ変わるなら馬か牛」は当然馬",
        "どんな物事に対しても、自分はある程度適応できると思う",
        "好き嫌いは多い方だ",
        "好きな数字は素数である",
        "本当にお金に困ったことがある"
    ]
}

# 選択肢とスコア配分
options = [
    "強く賛成", "賛成", "やや賛成", "どちらでもない", "やや反対", "反対", "強く反対"
]
score_map = {"強く賛成": 3, "賛成": 2, "やや賛成": 1, "どちらでもない": 0, "やや反対": -1, "反対": -2, "強く反対": -3}

# 各属性ごとに複数の質問をランダムで選択（セッションで保持）
NUM_QUESTIONS_PER_ATTRIBUTE = 4
if "selected_questions" not in st.session_state:
    selected_questions = []
    for key, questions in questions_dict.items():
        selected_questions.extend([(key, q) for q in random.sample(questions, NUM_QUESTIONS_PER_ATTRIBUTE)])
    random.shuffle(selected_questions)  # ここで質問を完全にランダムにする
    st.session_state.selected_questions = selected_questions
selected_questions = st.session_state.selected_questions

# 回答を保存する辞書
responses = {}
for i, (key, question) in enumerate(selected_questions):
    st.subheader(f"Q{i+1}: {question}")
    responses[f"{key}-{i}"] = st.radio("選択してください", options, index=3, key=f"q_{i}")

# 診断結果の計算
if st.button("診断結果を見る"):
    scores = {"S": 0, "N": 0, "A": 0, "Y": 0, "E": 0, "O": 0, "T": 0, "M": 0}
    neutral_count = 0
    
    for key, response in responses.items():
        if response == "どちらでもない":
            neutral_count += 1
        else:
            attr = key.rsplit("-", 1)[0]
            score = score_map[responses[key]]
            left_attr, right_attr = attr.split("-")
            
            if score > 0:
                scores[left_attr] += score
            elif score < 0:
                scores[right_attr] += abs(score)
    
    if neutral_count >= 10:
        result = "NOBU"
    else:
        result = ""
        result += "S" if scores["S"] >= scores["N"] else "N"
        result += "A" if scores["A"] >= scores["Y"] else "Y"
        result += "E" if scores["E"] >= scores["O"] else "O"
        result += "T" if scores["T"] >= scores["M"] else "M"
    
    st.success(f"あなたのタイプは {result} です！")
    
    # グラフの作成（端を揃えた割合グラフ）
    attributes = ["S-N", "A-Y", "E-O", "T-M"]
    left_values = [scores[attr[0]] for attr in attributes]
    right_values = [scores[attr[2]] for attr in attributes]
    total_values = [left + right if left + right > 0 else 1 for left, right in zip(left_values, right_values)]
    
    left_percents = [left / total * 100 for left, total in zip(left_values, total_values)]
    right_percents = [right / total * 100 for right, total in zip(right_values, total_values)]
    
    fig, ax = plt.subplots(figsize=(8, 5))
    y_pos = np.arange(len(attributes))
    
    ax.barh(y_pos, left_percents, color='blue', label='(S, A, E, T)')
    ax.barh(y_pos, right_percents, color='red', left=[100 - x for x in right_percents], label='(N, Y, O, M)')
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(attributes)
    ax.set_xlabel("percentage (%)")
    ax.set_xlim(0, 100)
    ax.legend()
    
    st.pyplot(fig)

# Streamlitの実行方法
# ターミナルで `streamlit run ファイル名.py` を実行してください