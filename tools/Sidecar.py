from flask import Flask

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    return 'hello world'

if __name__ == '__main__':
    app.run("0.0.0.0", debug=True, port=6006)