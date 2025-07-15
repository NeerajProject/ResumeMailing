from django.contrib import admin
from .models import MailingList, Contact, EmailTemplate, Mailing, MailingLog

admin.site.register(MailingList)
admin.site.register(Contact)
admin.site.register(EmailTemplate)
admin.site.register(Mailing)
admin.site.register(MailingLog)

