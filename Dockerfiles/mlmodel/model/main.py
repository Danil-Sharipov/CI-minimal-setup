from flask import Flask, request, jsonify
from forecast import main, predict

app = Flask(__name__)

@app.route('/add', methods = ['POST'])
def add():
    data = request.get_json(force=True)
    main(data)
    return 'True'

@app.route('/predict', methods = ['POST'])
def prediction():
    data = request.get_json(force=True)
    return jsonify(data=predict(data))
    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)