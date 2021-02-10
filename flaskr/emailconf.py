from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from flaskr.db import get_db
import os
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
            ping = f'ping {dominio} -c 1 '
            #grep = | grep -oE "([0-9]{1,3}[\.]){3}[0-9]{1,3})" | head -n 1
            ipdominio = os.system(ping)
            #db = get_db()
            error = None
            vpsname = "server.com"
            """vpsname = db.execute(
                'SELECT vpsname FROM vps WHERE ip = ?', (ipwebmail,)
            ).fetchone()
            if vpsname == None:
                vpsname = db.execute(
                    'SELECT vpsname FROM vps WHERE ip = ?', (ipdominio,)
                ).fetchone()"""
        if error != None:
            flash(error)
        return render_template('email/emailconf.html', protocol=protocol, email=email, vpsname=vpsname, inport=inport, outport=outport)
    return render_template('email/emailform.html')