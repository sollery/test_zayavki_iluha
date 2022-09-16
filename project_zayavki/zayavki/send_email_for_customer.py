import weasyprint
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from io import BytesIO


def send_email_customer(zayavka,mail,date,facality,fio,position):
    subject = 'Заявка'
    message = 'Информация по вашему заявке.'
    email = EmailMessage(subject,
                         message,
                         'ilushamdmaa@yandex.ru',
                         [mail])
    # Формирование PDF.
    html = render_to_string('pdf.html', {'data': zayavka, 'date':date, 'facality': facality,'fio' : fio,'position': position })
    out = BytesIO()
    stylesheets = [weasyprint.CSS('static/css/css_pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    # Прикрепляем PDF к электронному сообщению.
    email.attach('Заявка.pdf',
                 out.getvalue(),
                 'application/pdf')
    # Отправка сообщения.
    return email.send()