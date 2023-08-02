from dbClass import *
# read---------------------------------------------------------


@app.route('/')
def index():
    # menampilkan data terbaru
    dataKomposter = Komposter.query.order_by(
        Komposter.timestamp.desc()).first()

    # fluktuasi data sensor
    # sensor temperature
    last_count_day = dataKomposter.count_day
    if last_count_day > 1:
        sinceDataLastDay = Komposter.query.filter_by(
            count_day=last_count_day-1).all()
        sinceDataToDay = Komposter.query.filter_by(
            count_day=last_count_day).all()

        avarageTemperatureLastDay = sum(
            data.temperature for data in sinceDataLastDay) / len(sinceDataLastDay)
        avarageTemperatureToDay = sum(
            data.temperature for data in sinceDataToDay) / len(sinceDataToDay)

        flukTemperature = round(avarageTemperatureToDay -
                                avarageTemperatureLastDay, 1)

        # sensor moisture
        avarageMoistureLastDay = sum(
            data.moisture for data in sinceDataLastDay) / len(sinceDataLastDay)
        avarageMoistureToDay = sum(
            data.moisture for data in sinceDataToDay) / len(sinceDataToDay)

        flukMoisture = round(avarageMoistureToDay -
                             avarageMoistureLastDay, 1)

        # sensor ph_meter
        avaragePh_meterLastDay = sum(
            data.ph_meter for data in sinceDataLastDay) / len(sinceDataLastDay)
        avaragePh_meterToDay = sum(
            data.ph_meter for data in sinceDataToDay) / len(sinceDataToDay)

        flukPhMmeter = round(avaragePh_meterToDay -
                             avaragePh_meterLastDay, 1)

        # count day
        count_day = 30 - last_count_day

        # fluktuasi data sensor
        fluktuasi = {
            'temperature': flukTemperature,
            'moisture': flukMoisture,
            'ph_meter': flukPhMmeter,
            'count_day': count_day,
        }
    else:
        fluktuasi = {
            'temperature': 0,
            'moisture': 0,
            'ph_meter': 0,
            'count_day': 30,
        }

    # menampilkan 5 data terbaru
    lastdata = Komposter.query.order_by(
        Komposter.timestamp.desc()).limit(5).all()

    # menampilkan 9 data terbaru
    grafikKomposter = Komposter.query.order_by(
        Komposter.timestamp.desc()).limit(10).all()

    # Konversi data menjadi format JSON
    grafik_json = []
    for item in grafikKomposter:
        grafik_json.append({
            'label': item.timestamp.strftime('%H:%M'),
            'temperature': item.temperature,
            'moisture': item.moisture,
            'ph_meter': item.ph_meter
        })

    return render_template('index.html', data=dataKomposter, grafik=grafik_json, lastdata=lastdata, fluktuasi=fluktuasi)


@app.route('/tabel')
def tabel():
    # menampilkan data dari yang terbaru
    dataKomposter = dataKomposter = Komposter.query.order_by(
        Komposter.timestamp.desc()).all()

    return render_template('tabel.html', data=dataKomposter)


@app.route('/device')
def device():
    return render_template('device.html')

# create-------------------------------------------------------


if __name__ == '__main__':
    # Launch the application
    app.run(host='127.0.0.1', port=8001, debug=True)
