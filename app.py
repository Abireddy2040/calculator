from flask import Flask, request, jsonify, Response

app = Flask(__name__)

# Serve HTML directly
@app.route("/")
def index():
    return Response("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask Calculator</title>
        <style>
            body { font-family: Arial; text-align: center; margin-top: 50px; }
            #calculator { display: inline-block; border: 1px solid #ccc; padding: 20px; border-radius: 10px; }
            input { width: 200px; height: 40px; font-size: 18px; margin-bottom: 10px; }
            button { width: 45px; height: 45px; font-size: 18px; margin: 2px; }
        </style>
    </head>
    <body>
        <div id="calculator">
            <input type="text" id="display" readonly />
            <br>
            <button onclick="press('1')">1</button>
            <button onclick="press('2')">2</button>
            <button onclick="press('3')">3</button>
            <button onclick="press('+')">+</button><br>
            <button onclick="press('4')">4</button>
            <button onclick="press('5')">5</button>
            <button onclick="press('6')">6</button>
            <button onclick="press('-')">-</button><br>
            <button onclick="press('7')">7</button>
            <button onclick="press('8')">8</button>
            <button onclick="press('9')">9</button>
            <button onclick="press('*')">*</button><br>
            <button onclick="press('0')">0</button>
            <button onclick="press('.')">.</button>
            <button onclick="calculate()">=</button>
            <button onclick="press('/')">/</button><br>
            <button onclick="clearDisplay()">C</button>
        </div>

        <script>
            function press(char) {
                document.getElementById('display').value += char;
            }

            function clearDisplay() {
                document.getElementById('display').value = '';
            }

            function calculate() {
                fetch('/calculate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ expression: document.getElementById('display').value })
                })
                .then(res => res.json())
                .then(data => {
                    document.getElementById('display').value = data.result;
                })
                .catch(() => {
                    document.getElementById('display').value = 'Error';
                });
            }
        </script>
    </body>
    </html>
    """, mimetype='text/html')

# Endpoint to calculate expression
@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    expression = data.get("expression", "")
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return jsonify({"result": result})
    except:
        return jsonify({"result": "Error"})

if __name__ == "__main__":
    app.run(debug=True)
