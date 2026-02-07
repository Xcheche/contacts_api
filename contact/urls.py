from django.urls import path
from .views import ContactList, ContactDetail


urlpatterns = [
    path('', ContactList.as_view(), name='contact-list'),
    path('contacts/<int:id>/', ContactDetail.as_view(), name='contact-detail'),
]