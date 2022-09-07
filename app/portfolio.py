from flask import (
    Blueprint, render_template, request, redirect, url_for, current_app
)
import sendgrid
from sendgrid.helpers.mail import *

bp = Blueprint('portfolio', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    return render_template('portfolio/index.html')

@bp.route('/mail', methods=['GET', 'POST'])
def mail():
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')

    if request.method== 'POST':
        send_email(name, email, content)
        return render_template('portfolio/send_mail.html')
    return redirect(url_for('portfolio.index'))

def send_email(name, email, content):
    my_email = current_app.config['MY_EMAIL']
    sg = sendgrid.SendGridAPIClient(api_key=current_app.config['SENDGRID_API_KEY'])

    from_email = Email(my_email)
    to_email = To(my_email, substitutions={
        "-name-": name,
        "-email-": email,
        "-content-": content,
    })

    html_content = """
        <p>Hola Carlos, tienes un nuevo contacto desde la web:</p>
        <p>Nombre: -name-</p>
        <p>Correo: -email-</p>
        <p>Mensaje: -content-</p>
    """
    mail = Mail(my_email, to_email, 'Nuevo contacto desde la web', html_content=html_content)
    response_mail = mail.get()
    response_mail['personalizations']=None
    response = sg.client.mail.send.post(request_body=response_mail)
