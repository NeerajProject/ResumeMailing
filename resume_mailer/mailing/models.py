from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    company_name = models.CharField(max_length=255, blank=True)
    opt_out = models.BooleanField(default=False)
    subscription_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class MailingList(models.Model):
    name = models.CharField(max_length=255)
    contacts = models.ManyToManyField(Contact, related_name='mailing_lists')

    def __str__(self):
        return self.name

class Mailing(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('in_queue', 'In Queue'),
        ('sending', 'Sending'),
        ('sent', 'Sent'),
    )
    subject = models.CharField(max_length=255)
    body = models.TextField()
    mailing_lists = models.ManyToManyField(MailingList)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

class MailingAttachment(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='mailing_attachments/')

    def __str__(self):
        return self.file.name

class MailingLog(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='logs')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    sent = models.BooleanField(default=False)
    opened = models.BooleanField(default=False)
    clicked = models.BooleanField(default=False)
    replied = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contact.email} - {self.mailing.subject}"
