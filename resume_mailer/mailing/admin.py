from django.contrib import admin
from .models import Contact, MailingList, Mailing, MailingAttachment, MailingLog

class MailingAttachmentInline(admin.TabularInline):
    model = MailingAttachment
    extra = 1

class MailingLogInline(admin.TabularInline):
    model = MailingLog
    extra = 0
    readonly_fields = ('contact', 'sent', 'opened', 'clicked', 'replied', 'sent_at')
    can_delete = False

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'company_name', 'opt_out', 'subscription_date')
    search_fields = ('email', 'name', 'company_name')

@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('contacts',)

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('subject', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('subject', 'body')
    inlines = [MailingAttachmentInline, MailingLogInline]

@admin.register(MailingAttachment)
class MailingAttachmentAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'file')

@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'contact', 'sent', 'opened', 'clicked', 'replied', 'sent_at')
    readonly_fields = ('mailing', 'contact', 'sent', 'opened', 'clicked', 'replied', 'sent_at')
