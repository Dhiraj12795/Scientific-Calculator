from flask import Flask, request, jsonify, send_from_directory
import sympy as sp
import os
import math

app = Flask(__name__)

# Serve the index.html file when accessing the root URL
@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expression = data.get('expression', '').strip()

    if not expression:
        return jsonify({"error": "No expression provided"}), 400

    try:
        # Allow the following functions and constants from sympy and math
        allowed_locals = {
            'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan, 
            'sqrt': sp.sqrt, 'log': sp.log, 'pi': sp.pi, 
            'E': sp.E, 'exp': sp.exp, 'Abs': sp.Abs,
            'acos': sp.acos, 'asin': sp.asin, 'atan': sp.atan,
            'degrees': sp.deg, 'radians': sp.rad
        }

        # Replace ^ with ** for exponentiation
        expression = expression.replace('^', '**')

        # Evaluate the expression using eval with the allowed locals
        result = eval(expression, {"__builtins__": None}, allowed_locals)

        # If the result is a sympy object, we convert it to a float if it's a number
        if isinstance(result, sp.Basic):
            result = result.evalf()

        return jsonify({"result": str(result)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Use the port defined by Heroku or default to 6700 for local testing
    port = int(os.environ.get('PORT', 6700))
    app.run(debug=True, host='0.0.0.0', port=port)

