from flask import render_template, redirect, request, session, flash
from flask_app.models.instrument import Instrument
from flask_app.models.user import User
from flask_app import app

@app.route('/update/instrument/<int:id>')
def edit_instrument(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={ 
        "id":id
    }
    instrument=Instrument.get_instrument(data)
    return render_template("edit_instrument.html", instrument= instrument)

@app.route('/update/instruments', methods=['POST'])
def create_instrument():
    data = {
        'instrument' : request.form['instrument'],
        'years' : request.form['years'],
        'user_id' : session['user_id']
    }
    Instrument.save(data)
    return redirect('/home')