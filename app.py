from flask import Flask, render_template_string, request

app = Flask(__name__)

# Basic HTML web layout for the calculator buttons and styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>DevOps Flask Calculator</title>
    <style>
        body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #f0f2f5; margin: 0; }
        .calculator { background: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0px 4px 15px rgba(0,0,0,0.1); width: 300px; }
        .display { width: 100%; height: 50px; background: #222; color: #fff; text-align: right; font-size: 24px; padding: 5px 10px; box-sizing: border-box; border-radius: 6px; margin-bottom: 15px; border: none; }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
        button { height: 50px; font-size: 18px; border: none; border-radius: 6px; background: #e4e6eb; cursor: pointer; transition: 0.2s; }
        button:hover { background: #d8dadf; }
        .operator { background: #ff9f0a; color: white; }
        .operator:hover { background: #e08b07; }
        .clear { background: #f02849; color: white; }
        .clear:hover { background: #c81c37; }
    </style>
</head>
<body>
    <div class="calculator">
        <h3 style="margin-top:0; text-align:center; color:#333;">DevOps Smart Calculator</h3>
        <form method="POST">
            <input type="text" class="display" name="display" value="{{ result }}" readonly>
            <div class="grid">
                <button type="submit" name="action" value="C" class="clear">C</button>
                <button type="submit" name="action" value="(" class="operator">(</button>
                <button type="submit" name="action" value=")" class="operatorTracking">)</button>
                <button type="submit" name="action" value="/" class="operator">/</button>
                
                <button type="submit" name="action" value="7">7</button>
                <button type="submit" name="action" value="8">8</button>
                <button type="submit" name="action" value="9">9</button>
                <button type="submit" name="action" value="*" class="operator">*</button>
                
                <button type="submit" name="action" value="4">4</button>
                <button type="submit" name="action" value="5">5</button>
                <button type="submit" name="action" value="6">6</button>
                <button type="submit" name="action" value="-" class="operator">-</button>
                
                <button type="submit" name="action" value="1">1</button>
                <button type="submit" name="action" value="2">2</button>
                <button type="submit" name="action" value="3">3</button>
                <button type="submit" name="action" value="+" class="operator">+</button>
                
                <button type="submit" name="action" value="0" style="grid-column: span 2;">0</button>
                <button type="submit" name="action" value=".">.</button>
                <button type="submit" name="action" value="=" class="operator">=</button>
            </div>
        </form>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def calculator():
    current_expr = ""
    if request.method == 'POST':
        current_expr = request.form.get('display', '')
        action = request.form.get('action')

        if action == 'C':
            current_expr = ""
        elif action == '=':
            try:
                if current_expr:
                    current_expr = str(eval(current_expr))
            except Exception:
                current_expr = "Error"
        else:
            if current_expr == "Error":
                current_expr = ""
            current_expr += str(action)

    return render_template_string(HTML_TEMPLATE, result=current_expr)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

