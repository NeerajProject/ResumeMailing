from django.db import models

class MailingList(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Contact(models.Model):
    mailing_list = models.ForeignKey(MailingList, on_delete=models.CASCADE, related_name="contacts")
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} ({self.email})"

class EmailTemplate(models.Model):
    name = models.CharField(max_length=150)
    subject = models.CharField(max_length=200)
    html_content = models.TextField()

    def __str__(self):
        return self.name

class Mailing(models.Model):
    name = models.CharField(max_length=150)
    mailing_list = models.ForeignKey(MailingList, on_delete=models.CASCADE)
    template = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, null=True)
    from_email = models.EmailField()
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class MailingLog(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='Sent')
    sent_at = models.DateTimeField(auto_now_add=True)
