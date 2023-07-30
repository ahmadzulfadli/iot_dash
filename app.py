'''
http://127.0.0.1:7008/input_sensor?temperature=30&humidity=79
'''

from flask import Flask, render_template, redirect, url_for, request, flash

# read---------------------------------------------------------
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tabel')
def tabel():
    sensor_data = [
        {
            'temperature': 23,
            'humidity': 78,
        },
        {
            'temperature': 23,
            'humidity': 77,
        },
    ]

    return render_template('tabel.html', data=sensor_data)


@app.route('/device')
def device():
    sensor_data = [
        {
            'temperature': 23,
            'humidity': 78,
        },
        {
            'temperature': 23,
            'humidity': 77,
        },
    ]

    return render_template('device.html', data=sensor_data)

# create-------------------------------------------------------


if __name__ == '__main__':
    # Launch the application
    app.run(host='127.0.0.1', port=8001, debug=True)
