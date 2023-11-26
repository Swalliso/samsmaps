from flask import Flask, render_template, request
from map_generator import generate_and_display_map

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_map', methods=['POST'])
def generate_map():
    rows = int(request.form.get('rows', 16))
    cols = int(request.form.get('cols', 16))
    map_filename = 'static/map.png'
    generate_and_display_map(rows, cols, filename=map_filename)
    return render_template('map.html', map_image=map_filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
