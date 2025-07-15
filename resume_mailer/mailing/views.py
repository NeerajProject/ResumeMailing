from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Contact, MailingList, Mailing, MailingAttachment, MailingLog
from .forms import ContactForm, MailingListForm, MailingForm

# Contact CRUD
@login_required
def contact_list(request):
    search = request.GET.get('q', '')
    contacts = Contact.objects.filter(Q(name__icontains=search) | Q(email__icontains=search))
    return render(request, 'mailing/contact_list.html', {'contacts': contacts, 'search': search})

@login_required
def contact_create(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('mailing:contact_list')
    return render(request, 'mailing/contact_form.html', {'form': form})

@login_required
def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    form = ContactForm(request.POST or None, instance=contact)
    if form.is_valid():
        form.save()
        return redirect('mailing:contact_list')
    return render(request, 'mailing/contact_form.html', {'form': form})

@login_required
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('mailing:contact_list')
    return render(request, 'mailing/contact_confirm_delete.html', {'contact': contact})

# MailingList CRUD
@login_required
def mailinglist_list(request):
    search = request.GET.get('q', '')
    lists = MailingList.objects.filter(name__icontains=search)
    return render(request, 'mailing/mailinglist_list.html', {'lists': lists, 'search': search})

@login_required
def mailinglist_create(request):
    form = MailingListForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('mailing:mailinglist_list')
    return render(request, 'mailing/mailinglist_form.html', {'form': form})

@login_required
def mailinglist_edit(request, pk):
    ml = get_object_or_404(MailingList, pk=pk)
    form = MailingListForm(request.POST or None, instance=ml)
    if form.is_valid():
        form.save()
        return redirect('mailing:mailinglist_list')
    return render(request, 'mailing/mailinglist_form.html', {'form': form})

@login_required
def mailinglist_delete(request, pk):
    ml = get_object_or_404(MailingList, pk=pk)
    if request.method == 'POST':
        ml.delete()
        return redirect('mailing:mailinglist_list')
    return render(request, 'mailing/mailinglist_confirm_delete.html', {'mailinglist': ml})

# Mailing CRUD + Attachments + Kanban
@login_required
def mailing_list(request):
    search = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')

    mailings = Mailing.objects.all()
    if search:
        mailings = mailings.filter(Q(subject__icontains=search) | Q(body__icontains=search))
    if status_filter:
        mailings = mailings.filter(status=status_filter)

    return render(request, 'mailing/mailing_list.html', {'mailings': mailings, 'search': search, 'status_filter': status_filter})

@login_required
def mailing_create(request):
    form = MailingForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        mailing = form.save()
        for file in request.FILES.getlist('attachments'):
            MailingAttachment.objects.create(mailing=mailing, file=file)
        return redirect('mailing:mailing_list')
    return render(request, 'mailing/mailing_form.html', {'form': form})

@login_required
def mailing_edit(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    form = MailingForm(request.POST or None, request.FILES or None, instance=mailing)
    if form.is_valid():
        form.save()
        for file in request.FILES.getlist('attachments'):
            MailingAttachment.objects.create(mailing=mailing, file=file)
        return redirect('mailing:mailing_list')
    return render(request, 'mailing/mailing_form.html', {'form': form, 'mailing': mailing})

@login_required
def mailing_delete(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if request.method == 'POST':
        mailing.delete()
        return redirect('mailing:mailing_list')
    return render(request, 'mailing/mailing_confirm_delete.html', {'mailing': mailing})

@login_required
def mailing_kanban(request):
    search = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')

    mailings = Mailing.objects.all()
    if search:
        mailings = mailings.filter(subject__icontains=search)
    if status_filter:
        mailings = mailings.filter(status=status_filter)

    return render(request, 'mailing/mailing_kanban.html', {'mailings': mailings, 'search': search, 'status_filter': status_filter})

# Mailing Logs (Read-only)
@login_required
def mailinglog_list(request):
    logs = MailingLog.objects.select_related('mailing', 'contact').all()
    return render(request, 'mailing/mailinglog_list.html', {'logs': logs})
