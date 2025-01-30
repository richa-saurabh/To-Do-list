from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database initialization
def init_db():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  task TEXT NOT NULL,
                  category TEXT,
                  due_date TEXT,
                  completed BOOLEAN DEFAULT 0)''')
    conn.commit()
    conn.close()

# Home route - Display all tasks
@app.route('/')
def index():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Add a new task
@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    category = request.form['category']
    due_date = request.form['due_date']
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task, category, due_date) VALUES (?, ?, ?)",
              (task, category, due_date))
    conn.commit()
    conn.close()
    flash('Task added successfully!', 'success')
    return redirect(url_for('index'))

# Mark a task as completed
@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    flash('Task marked as completed!', 'success')
    return redirect(url_for('index'))

# Edit a task
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    if request.method == 'POST':
        task = request.form['task']
        category = request.form['category']
        due_date = request.form['due_date']
        c.execute("UPDATE tasks SET task = ?, category = ?, due_date = ? WHERE id = ?",
                  (task, category, due_date, task_id))
        conn.commit()
        conn.close()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('index'))
    else:
        c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = c.fetchone()
        conn.close()
        return render_template('edit.html', task=task)

# Delete a task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)