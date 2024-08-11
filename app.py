from flask import Flask, render_template, request, redirect, url_for

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# 仮のデータベースとして、タスクを格納するリストを用意
tasks = []

# ルートURLにアクセスした際の処理
@app.route('/')
def index():
    # `index.html` テンプレートをレンダリングし、`tasks` リストを渡す
    return render_template('index.html', tasks=tasks)

# 新しいタスクを追加するためのルート
@app.route('/add', methods=['POST'])
def add_task():
    # フォームから送信されたタスクを取得
    task = request.form.get('task')
    # タスクが空でない場合はリストに追加
    if task:
        tasks.append(task)
    # メインページにリダイレクト
    return redirect(url_for('index'))

# タスクを削除するためのルート
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    # タスクIDがリストの範囲内であれば、該当タスクを削除
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    # メインページにリダイレクト
    return redirect(url_for('index'))

# アプリケーションのエントリーポイント
if __name__ == '__main__':
    # デバッグモードでアプリケーションを起動
    app.run(debug=True)
