from flask import render_template, redirect, request, session, flash
from flask_app.models.instrument import Instrument
from flask_app.models.user import User
from flask_app import app

@app.route('/update/instrument')
def edit_instrument():
    if 'user_id' not in session:
        return redirect('/logout')
    instruments = Instrument.get_all_instruments()
    return render_template("edit_instrument.html", instruments=instruments )

@app.route('/update/instruments', methods=['POST'])
def create_instrument():
    data = {
        'instrument' : request.form['instrument'],
        'years' : request.form['years'],
        'user_id' : session['user_id']
    }
    Instrument.save(data)
    return redirect('/home')

@app.route('/remove')
def remove_instrument():
    Instrument.remove()
    return redirect('/update/instrument')