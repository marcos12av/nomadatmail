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
        ipwebmail = validaip(email)
        error = None
        if ipwebmail is None:
            error = f'Cuenta de correo {email} no esta en nuestros sistemas'
        else:
            db = get_db()
            row = db.execute(
                'SELECT * FROM vps WHERE ip = ?', (ipwebmail,)
            ).fetchone()
            if row is None:
                error = f'Cuenta de correo no esta en nuestros sistemas'
            else:
                if protocol == "IMAP":
                    inport = "993, con SSL"
                    outport = "465 o 587, con SSL"
                elif protocol == "POP": 
                    inport = "995, con SSL"
                    outport = "465 o 587, con SSL"
                vpsname = row['vpsname']
                consul = True
                return render_template('email/emailconf.html', protocol=protocol, email=email, vpsname=vpsname, inport=inport, outport=outport, consul=consul)
        return render_template('email/emailconf.html', error=error)
    return render_template('email/emailconf.html')

def validaip(email):
    dominio = "webmail." + email[(email.find("@")+1):]
    ping = ['ping', '-c', '1', dominio]
    runping = subprocess.run(ping, capture_output=True, text=True)
    if runping.stdout:
        ipregex = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", runping.stdout)
        return ipregex.group(0)
    else:
        return None
    
