from flask import Flask, render_template, request, redirect, jsonify
import sqlite3, os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# DATABASE INIT
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS apps
                 (id INTEGER PRIMARY KEY,
                  name TEXT,
                  description TEXT,
                  file TEXT,
                  downloads INTEGER)''')
    conn.commit()
    conn.close()

init_db()

# HOME PAGE
@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    apps = c.execute("SELECT * FROM apps").fetchall()
    conn.close()
    return render_template('index.html', apps=apps)

# DOWNLOAD
@app.route('/download/<int:id>')
def download(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE apps SET downloads = downloads + 1 WHERE id=?", (id,))
    conn.commit()
    app_data = c.execute("SELECT file FROM apps WHERE id=?", (id,)).fetchone()
    conn.close()
    return redirect("/uploads/" + app_data[0])

# ADMIN PANEL
@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['desc']
        file = request.files['file']

        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO apps (name, description, file, downloads) VALUES (?,?,?,0)",
                  (name, desc, filename))
        conn.commit()
        conn.close()

        return redirect('/admin')

    return render_template('admin.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)