from flask import Flask, request, jsonify
import numpy as np
from add import main as m

app = Flask(__name__)

@app.route('/add', methods = ['POST'])
def add():
    data = request.get_json(force=True)
    print(m(data))
    return 'True'
    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)