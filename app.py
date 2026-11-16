from flask import Flask, render_template
from controllers.abb_controller import abb_bp
from controllers.expresion_controller import expresion_bp

app = Flask(__name__)
app.register_blueprint(abb_bp)
app.register_blueprint(expresion_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)