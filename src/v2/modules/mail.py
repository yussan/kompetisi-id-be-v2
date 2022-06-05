import app
from flask_mail import Message
from flask import render_template, Markup


def sendEmail(title, body, target):
     # ref: https: // pythonhosted.org/Flask-Mail/
    msg = Message(title,
                  sender="noreply@kompetisi.id",
                  recipients=target)
    # msg.html = body
    # location: /v2/email/index.html
    msg.html = render_template(
        'email/index.html', body=Markup(body))
    return app.mail.send(msg)
# try:
#     # ref: https: // pythonhosted.org/Flask-Mail/
#     msg = Message(title,
#                   sender="noreply@kompetisi.id",
#                   recipients=target)
#     msg.html = render_template('email/index.html', body=Markup(body))
#     return app.mail.send(msg)
# except NameError:
#     print("[ERROR] Error sending email....")
#     print(NameError)
#     return True
