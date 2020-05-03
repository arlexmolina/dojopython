from flask import render_template
from flask_mail import Message

from app import logger
from app import mail

#borrar
def send_async_email(msg_dict):
    msg = Message()
    msg.__dict__.update(msg_dict)
    mail.send(msg)

def send_async_emails(msg_dicts):
    with mail.connect() as conn:
        for msg_dict in msg_dicts:
            msg = Message()
            msg.__dict__.update(msg_dict)
            conn.send(msg)


def send_email(to, subject, template, **kwargs):
    logger.info(" ")
    logger.info("Correo enviado a: " + str(to))
    logger.info(" ")

    msg_dict = message_to_dict(to, subject, template, **kwargs)
    send_async_email.delay(msg_dict)


def message_to_dict(to, subject, template, **kwargs):
    msg = Message(subject='[RESERVA] ' + subject,
                  sender=('app empresariales', 'materiapps@gmail.com'),
                  recipients=to)
    msg.body = render_template('emails/' + template + '.txt', **kwargs)
    msg.html = render_template('emails/' + template + '.html', **kwargs)
    return msg.__dict__
