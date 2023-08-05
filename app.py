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


@app.route('/inputData', methods=['GET'])
def inputData():
    try:
        mode = request.args.get('mode')
        if mode != 'save':
            return jsonify({"error": "Mode not found."}), 400

        else:
            temperature = request.args.get('temperature', type=float)
            moisture = request.args.get('moisture', type=float)
            ph_meter = request.args.get('ph_meter', type=float)
            count_day = request.args.get('count_day', type=int)

            if temperature is None or moisture is None or ph_meter is None or count_day is None:
                return jsonify({"error": "Temperature or moisture or ph_meter or count_day parameters are required."}), 400

            # Lakukan operasi simpan data ke database atau lakukan tindakan sesuai kebutuhan
            newKomposter = Komposter(
                temperature=temperature,
                moisture=moisture,
                ph_meter=ph_meter,
                count_day=count_day,
            )

            # Tambahkan data baru ke session
            db.session.add(newKomposter)
            # Commit session untuk menyimpan perubahan data ke database
            db.session.commit()

            return redirect(url_for('lihatData'))

    except Exception as e:
        return jsonify({"error": "An error occurred while trying to add sensor data."}), 500


@app.route('/lihatData', methods=['GET'])
def lihatData():
    # tampilkan seluruh database dalam format json
    dataKomposter = Komposter.query.order_by(
        Komposter.timestamp.desc()).all()
    data = []
    for item in dataKomposter:
        data.append({
            'id': item.id,
            'temperature': item.temperature,
            'moisture': item.moisture,
            'ph_meter': item.ph_meter,
            'count_day': item.count_day,
            'timestamp': item.timestamp.strftime('%H:%M'),
        })

    response = {
        "status": "success",
        "message": "Sensor data added successfully!",
        "data": data
    }

    return jsonify(response), 200


if __name__ == '__main__':
    # Launch the application
    app.run()
