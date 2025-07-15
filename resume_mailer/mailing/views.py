from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from .models import Mailing, MailingLog
from .forms import MailingForm

def create_mailing(request):
    if request.method == 'POST':
        form = MailingForm(request.POST, request.FILES)
        if form.is_valid():
            mailing = form.save()

            recipients = mailing.mailing_list.contacts.all()

            for contact in recipients:
                email = EmailMessage(
                    subject=mailing.template.subject,
                    body=mailing.template.html_content,
                    from_email=mailing.from_email,
                    to=[contact.email],
                )
                email.content_subtype = "html"

                if mailing.attachment:
                    email.attach(
                        mailing.attachment.name,
                        mailing.attachment.read(),
                        mailing.attachment.file.content_type
                    )

                email.send()

                MailingLog.objects.create(
                    mailing=mailing,
                    contact=contact,
                    status='Sent'
                )

            mailing.sent = True
            mailing.save()

            return redirect('mailing_success')
    else:
        form = MailingForm()
    return render(request, 'mailing/create_mailing.html', {'form': form})

def mailing_success(request):
    return render(request, 'mailing/success.html')
