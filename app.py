from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# SQLiteデータベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemyインスタンスを作成
db = SQLAlchemy(app)

# タスクのデータベースモデルを定義
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Task {self.id}: {self.content}>'

# 初回実行時にデータベースを作成
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # データベースから全てのタスクを取得
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    # フォームから送信されたタスクを取得
    task_content = request.form.get('task')
    if task_content:
        # 新しいタスクをデータベースに追加
        new_task = Task(content=task_content)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    # 編集するタスクを取得
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        # フォームから送信された新しいタスク内容を取得
        new_content = request.form.get('task')
        if new_content:
            task.content = new_content
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('edit.html', task=task)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    # 指定されたIDのタスクをデータベースから削除
    task_to_delete = Task.query.get_or_404(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
