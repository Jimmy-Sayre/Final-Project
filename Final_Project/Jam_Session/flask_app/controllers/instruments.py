from flask import render_template, redirect, request, session, flash
from flask_app.models.instrument import Instrument
from flask_app.models.user import User
from flask_app import app

@app.route('/edit/instrument')
def edit_instrument():
    instrument=Instrument.get_instrument()
    return render_template("edit_instrument.html", instrument= instrument)