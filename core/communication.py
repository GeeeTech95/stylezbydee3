
from django.shortcuts import render
from django.views.generic import RedirectView,View
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string,get_template
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
#import imgkit
from io import BytesIO
#from  xhtml2pdf import pisa
import random
#from twilio.rest import Client
from django.core.mail import EmailMultiAlternatives, SafeMIMEMultipart
from email.mime.image import MIMEImage

from core.templatetags.vocabulary import capitalize
import os




class AccountMail() :
    def __init__(self,user) :
        self.user = user

    def send_user_credentials(self) :
        mail = Email("support")
        message = "Your Email :  {}, Your account Id : {}".format(self.user.email,self.user.account_id)
        mail.send_email(
            [self.user.email],
            subject = "{} User Credentials".format(settings.SITE_NAME),
            message= message,
        
            )  

      
    def send_registration_email(self) :
        mail = Email("support")
     
        mail.send_html_email(
            [self.user.email],
            template="email/registration/registration-mail.html",
            subject = "Welcome to {}".format(settings.SITE_NAME),
            ctx = {"name" : self.user.full_name}
            )   


    def send_verification_code(self,email,code)   :
        mail = Email("security")
        mail.send_html_email(
            [email],
            template="verification-code-mail.html",
            subject = "{} Verification Code".format(settings.SITE_NAME),
            ctx = {"code" : code,"verification_code_validity" : 5 }
            )      





class Email() :
    def __init__(self,send_type = "support") :

        from django.core.mail import get_connection

        host = settings.EMAIL_HOST
        port = settings.EMAIL_PORT
        password = settings.EMAIL_HOST_PASSWORD

        senders = {
            'support' : settings.EMAIL_HOST_USER_SUPPORT,
            "security" : settings.EMAIL_HOST_USER_SUPPORT,
            "logistics" : settings.EMAIL_HOST_USER_LOGISTICS,
        }

        if not send_type :
           self.send_from = senders['support']

        else :
            self.send_from = senders.get(send_type,senders['support'])
        
        self.auth_connecion = get_connection(
            host = host,
            port = port,
            username = self.send_from,
            password = password,
            use_tls = settings.EMAIL_USE_TLS
        ) 


    
    def send_email(self,receive_email_list,subject,message,headers=None) :
        headers = {
            'Content-Type' : 'text/plain'
        } 
        try : 
            email = EmailMessage(subject = subject,body=message,
            from_email=self.send_from,to=receive_email_list,
            headers = headers,connection=self.auth_connecion)
            email.send()
            self.auth_connecion.close()
        except :
            pass


    def send_html_email(self,receive_email_list,template = None,subject =None,files_path_list=None,ctx=None) :
        error = None #for error control
        subject = subject or self.default_subject
        template = template or self.default_template
        ctx = ctx
        ctx['site_name'] = settings.SITE_NAME
        msg = render_to_string(template,ctx)
        
        email = EmailMultiAlternatives(
            subject,
            msg,
            self.send_from,
            receive_email_list,
            connection=self.auth_connecion
            )
        email.content_subtype = "html"
        email.mixed_subtype = "related"
 
        BASE_DIR = settings.STATIC_URL
        logo_path = os.path.join(settings.BASE_DIR,"static/img/logo/logo-black.png")
        with open(logo_path,'rb') as f :
            logo = MIMEImage(f.read())
            logo.add_header("Content-ID","<logo.png>")
            email.attach(logo)
            
    
        try :
            email.send()
        except : 
            error = "mail was not sent successfully"
            print(error)
        self.auth_connecion.close()
        
        return error
        
        


    def send_file_email(self,file_name,_file,receive_email_list,subject,message) :
        email = EmailMessage(subject,message,self.send_from,receive_email_list,connection=self.auth_connecion)
        email.attach(file_name,_file)
        try : 
            email.send()
            self.auth_connecion.close()
        except : pass


 

    





