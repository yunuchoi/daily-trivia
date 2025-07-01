from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/send_daily_trivia')
def run_trivia():
    try:
        subprocess.Popen([
            '/home/yunuchoi/jippilji-daily-trivia/venv-jippilji/bin/python',
            '/home/yunuchoi/jippilji-daily-trivia/jippilji.py'
        ])
        return 'Trivia script started successfully.', 200
    except Exception as e:
        return f'Error: {str(e)}', 500

if __name__ == '__main__':
    app.run()
