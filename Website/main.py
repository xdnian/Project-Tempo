from flask import Flask, Response

app = Flask(__name__, static_folder='html_public', static_url_path='')

@app.route('/hello')
def index():
    return "Hello World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2333, debug=True)