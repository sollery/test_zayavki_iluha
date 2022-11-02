import weasyprint
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from io import BytesIO
from accounts.models import CustomUser

def send_email_customer(zayavka,mail,date,fio,position,subdivision,count_rabotniki,viza_k):
    subject = 'Заявка'
    message = 'Информация по вашему заявке.'

    email = EmailMessage(subject,
                         message,
                         'ilyazakharovwow@gmail.com',
                         [mail])
    # Формирование PDF.
    html = render_to_string('pdf.html', {'data': zayavka, 'date':date, 'fio' : fio,'position': position, 'subdivision': subdivision,'count_rabotniki':count_rabotniki,'viza_k':viza_k})
    out = BytesIO()
    stylesheets = [weasyprint.CSS('static/css/css_pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    # Прикрепляем PDF к электронному сообщению.
    email.attach('Заявка.pdf',
                 out.getvalue(),
                 'application/pdf')
    # Отправка сообщения.
    return email.send()