from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from flaskr.db import get_db
import subprocess, re
bp = Blueprint('emailconf', __name__, url_prefix='/')

@bp.route('/', methods=('GET', 'POST'))
def emailconf():
    if request.method == 'POST':
        email = request.form['email']
        protocol = request.form['protocol']
        if protocol == "imap":
            inport = "5xxii"
            outport = "5xxio"
            error = None
        elif protocol == "pop": 
            inport = "5xxpi"
            outport = "5xxpo"
            error = None
        else:
            error = 'Datos no validos'
        if not email:
            error = 'Favor de ingresar un email valido'
        if error is None:
            dominio = "webmail." + email[(email.find("@")+1):]
            ping = ['ping', '-c', '1', dominio]
            runping = subprocess.run(ping, capture_output=True, text=True)
            ipregex = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", runping.stdout)
            ipwebmail = ipregex.group(0)
            
            db = get_db()
            error = None
            row = db.execute(
                'SELECT * FROM vps WHERE ip = ?', (ipwebmail,)
            ).fetchone()
            vpsname = row['vpsname']
        if error != None:
            flash(error)
        return render_template('email/emailconf.html', protocol=protocol, email=email, vpsname=vpsname, inport=inport, outport=outport)
    return render_template('email/emailform.html')