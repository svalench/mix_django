from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.exceptions import ValidationError

from mix_django.settings import DOMAIN, EMAIL_HOST_USER
from user.views import account_activation_token


class EmailSending:
    """
    Класс для отправки сообщений пользователям системы

    """

    def __init__(self):
        self.current_site = DOMAIN
        self.my_email = EMAIL_HOST_USER

    def send_cart_email(self, user, cart):
        mail_subject = 'Заказ на mixenerdgy'
        data = cart
        self.send_html_email('Заказ на mixenerdgy', 'email_template/order.html', data, user.email)


    def send_email_registration(self, user):
        """отправка сообщения при авторизации"""
        mail_subject = 'Activate your account.'
        data = {
            'domain': self.current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }
        self.send_mail('Активация аккаунта', 'email_template/email_activation_template.html', data, user.email)

    def send_email_forgot_password(self, user, password):
        """отправка письма с новым паролем"""
        data = {"newpassword": password, "name":user.first_name, "last_name":user.last_name}
        if(self.send_mail('Восстановления пароля', 'email_template/email_change_pass.html', data, user.email)):
            user.set_password(password)
            user.save()

    def send_mail(self, subject:str, template:str, data:dict, email:str) -> bool:
        """отправка письма пользователю"""
        mail_subject = subject
        message = render_to_string(template, data)
        try:
            send_mail(mail_subject, message, self.my_email, [email])
            return True
        except Exception as e:
            ValidationError({"detail": "Проблема отправки письма. Обратитесь к администратору."})
            return False

    def send_html_email(self,  subject:str, template:str, data:dict, email:str) -> bool:

        text_content = 'This is an important message.'
        html_content = render_to_string(template, data)
        msg = EmailMultiAlternatives(subject, text_content, self.my_email, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()