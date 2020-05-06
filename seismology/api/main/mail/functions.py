from flask current_app, render_template
from flask_mail import Message
from .. import mailsender
from smtlib import SMTPException

def sendMail(to, subject, template, **kwargs):
    msg = Message(subject, sender=current_app.["FLASKY_MAIL_SENDER"], recipients=[to])
    try:
        msg.body = render_template(template + ".txt", **kwargs)
        msg.html = render_template(template + ".html", **kwargs)
        result = mailsender.send(msg)
    except SMTPException as e:
        print(str(e))
        return "Mail deliver failed"
    return True