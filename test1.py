import streamlit as st
import pandas as pd

# st.session_stateにデータが存在しない場合は初期化
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame({"優先順位": [1], "提出期限": [pd.to_datetime("2023-01-01 00:00:00")], "タスク": ["text"]})

st.title('タスクスケジューラー')

# タスクを追加または編集するフィールド
new_date = st.date_input("提出期限 日付", value=pd.to_datetime("2023-01-01"))
new_time = st.time_input("提出期限 時間", value=pd.to_datetime("00:00:00").time())
new_rank = st.number_input("優先順位", min_value=1, value=1)
new_task = st.text_area("タスク内容", value="")

# タスクを追加または編集するボタン
add_or_edit_button = st.button("タスクを追加または編集")

if add_or_edit_button:
    # 新しいランクが既存のデータに存在する場合は編集、存在しない場合は追加
    if new_rank in st.session_state.df['優先順位'].values:
        dt_str = f"{new_date} {new_time.strftime('%H:%M:%S')}"
        st.session_state.df.loc[st.session_state.df['優先順位'] == new_rank, ['提出期限', 'タスク']] = [pd.to_datetime(dt_str), new_task]
        st.success(f"ランク {new_rank} のタスクを編集しました。")
    else:
        dt_str = f"{new_date} {new_time.strftime('%H:%M:%S')}"
        new_data = pd.DataFrame({"優先順位": [new_rank], "提出期限": [pd.to_datetime(dt_str)], "タスク": [new_task]})
        st.session_state.df = pd.concat([st.session_state.df, new_data], ignore_index=True)
        st.success(f"ランク {new_rank} のタスクを追加しました。")

# タスクを削除するフィールド
delete_rank = st.number_input("削除するタスクを選択", min_value=1, value=1)

# 削除ボタンが押されたらデータを削除
if st.button("タスクを削除"):
    st.session_state.df = st.session_state.df[st.session_state.df['優先順位'] != delete_rank]
    st.success(f"ランク {delete_rank} のタスクを削除しました。")

# タスクをソートするボタン
if st.button("タスクをソート"):
    st.session_state.df = st.session_state.df.sort_values(by=['優先順位', '提出期限'])

# タスク表のスタイルを変更するCSS
style = """
<style>
.table td:nth-child(3) {
    min-width: 400px;
    max-width: 800px;
    word-wrap: break-word;
}
</style>
"""
st.markdown(style, unsafe_allow_html=True)

# 提出期限を分単位で表示
st.write('タスク表:')
edited_df = st.table(st.session_state.df[['優先順位', '提出期限', 'タスク']])
edited_df.table.table_data[0]['column_formats'][1] = {
    'type': 'datetime',
    'format': '%Y-%m-%d %H:%M:%S'
}
