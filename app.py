from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Hello from your Docker container!</h1>"

if __name__ == '__main__':
    # host='0.0.0.0' allows outside connections
    app.run(host='0.0.0.0', port=5000)

