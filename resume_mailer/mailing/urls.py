from django.urls import path
from . import views

app_name = 'mailing'

urlpatterns = [
    path('accounts/profile/', views.dashboard, name='dashboard'),
    # Contact
    path('contacts/', views.contact_list, name='contact_list'),
    path('contacts/create/', views.contact_create, name='contact_create'),
    path('contacts/edit/<int:pk>/', views.contact_edit, name='contact_edit'),
    path('contacts/delete/<int:pk>/', views.contact_delete, name='contact_delete'),

    # Mailing List
    path('lists/', views.mailinglist_list, name='mailinglist_list'),
    path('lists/create/', views.mailinglist_create, name='mailinglist_create'),
    path('lists/edit/<int:pk>/', views.mailinglist_edit, name='mailinglist_edit'),
    path('lists/delete/<int:pk>/', views.mailinglist_delete, name='mailinglist_delete'),

    # Mailing
    path('mailings/', views.mailing_list, name='mailing_list'),
    path('mailings/create/', views.mailing_create, name='mailing_create'),
    path('mailings/edit/<int:pk>/', views.mailing_edit, name='mailing_edit'),
    path('mailings/delete/<int:pk>/', views.mailing_delete, name='mailing_delete'),
    path('mailings/kanban/', views.mailing_kanban, name='mailing_kanban'),

    # Logs
    path('logs/', views.mailinglog_list, name='mailinglog_list'),
]
