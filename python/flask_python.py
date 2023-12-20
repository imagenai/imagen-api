from flask import Flask, render_template, request, redirect, url_for
from typer_runner import run_gui

app = Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    input_dir = request.form['input_dir']
    output_dir = request.form['output_dir']
    profile_name = request.form['profile_name']
    api_key = request.form['api_key']

    run_gui(input_dir=input_dir, output_dir=output_dir, profile_name=profile_name, api_key=api_key)
    return redirect(url_for('success'))


@app.route('/success', methods=['GET'])
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)
