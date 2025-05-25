from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def game():
    return render_template('game.html')

# Pygame dosyaları için route
@app.route('/pygame/<path:filename>')
def pygame_files(filename):
    return send_from_directory('static/game', filename)

if __name__ == '__main__':
    app.run(debug=True)