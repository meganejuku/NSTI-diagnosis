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
        "よく計画を立てずに行動してしまう",
        "新しいことに挑戦するのが好きだ",
        "細かい部分より全体の流れを重視する",
        "直感的に物事を捉える方だ",
        "細かいディテールより全体のバランスを見て判断する"
    ],
    "A-Y": [
        "大人数の場では元気が出る方だ",
        "リスクを取ってでも面白そうなことをやりたい",
        "予想外の展開を楽しむタイプだ",
        "計画通りに進めるより、その場の流れで決める方が好き",
        "新しい環境にすぐ適応できる"
    ],
    "E-O": [
        "物事を深く考えすぎてしまうことがある",
        "慎重に行動することが多い",
        "物事の可能性や未来をよく想像する",
        "リスクを回避するために徹底的に準備をする",
        "何か決断をするときに、長く考えることが多い"
    ],
    "T-M": [
        "気分の浮き沈みが激しい方だ",
        "感情を素直に表現するタイプだ",
        "何事も冷静に対処しようとする",
        "物事に対して強い感情を抱きやすい",
        "周囲の感情や雰囲気に影響されやすい"
    ]
}

# 選択肢とスコア配分
options = [
    "強く賛成", "賛成", "やや賛成", "どちらでもない", "やや反対", "反対", "強く反対"
]
score_map = {"強く賛成": 3, "賛成": 2, "やや賛成": 1, "どちらでもない": 0, "やや反対": -1, "反対": -2, "強く反対": -3}

# 各属性ごとに複数の質問をランダムで選択（セッションで保持）
NUM_QUESTIONS_PER_ATTRIBUTE = 3
if "selected_questions" not in st.session_state:
    st.session_state.selected_questions = {
        key: random.sample(questions, NUM_QUESTIONS_PER_ATTRIBUTE) for key, questions in questions_dict.items()
    }
selected_questions = st.session_state.selected_questions

# 回答を保存する辞書
responses = {}
for key, questions in selected_questions.items():
    for i, question in enumerate(questions):
        st.subheader(f"{key}-{i+1}: {question}")
        responses[f"{key}-{i}"] = st.radio("選択してください", options, index=3, key=f"q_{key}_{i}")

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
    
    ax.barh(y_pos, left_percents, color='blue', label='左側 (S, A, E, T)')
    ax.barh(y_pos, right_percents, color='red', left=[100 - x for x in right_percents], label='右側 (N, Y, O, M)')
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(attributes)
    ax.set_xlabel("割合 (%)")
    ax.set_xlim(0, 100)
    ax.legend()
    
    st.pyplot(fig)

# Streamlitの実行方法
# ターミナルで `streamlit run ファイル名.py` を実行してください
