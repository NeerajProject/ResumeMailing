from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from .models import Mailing, MailingLog
from .forms import MailingForm

from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .forms import MailingForm
from .models import MailingLog

def create_mailing(request):
    if request.method == 'POST':
        form = MailingForm(request.POST, request.FILES)
        if form.is_valid():
            mailing = form.save()

            # Static subject and template
            subject = "Resume Submission for Your Review"
            html_content = render_to_string("mailing/emails/email_template.html")  # Fully static HTML

            recipients = mailing.mailing_list.contacts.all()

            for contact in recipients:
                email = EmailMessage(
                    subject=subject,
                    body=html_content,
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
