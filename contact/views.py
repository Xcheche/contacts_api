from config import settings
from contact.serializers import ContactSerializer
from .models import Contact
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from django.core.mail import send_mail  # type: ignore

# Create your views here.
#List  , Create 
class ContactList(ListCreateAPIView):

    serializer_class = ContactSerializer
    # permission_classes = [IsAuthenticated,]
    


    def perform_create(self, serializer):
        #serializer.save(owner=self.request.user)
        serializer.save()
        # Send email notification to the user
        send_mail(
            'New Contact Created',
            'A new contact has been created in your address book.',
            settings.EMAIL_HOST_USER,
            [self.request.user.email],
            fail_silently=False,
        )

        

    def get_queryset(self):   
        #return  Contact.objects.filter(owner=self.request.user)  
        return  Contact.objects.all()
    
#Detail , Update, Delete
class ContactDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


    def get_queryset(self):   
        return  Contact.objects.filter(owner=self.request.user)    
    
    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

        # Send email notification to the user
        send_mail(
            'Contact Updated',
            'A contact has been updated in your address book.',
            settings.EMAIL_HOST_USER,
            [self.request.user.email],
            fail_silently=False,
        )

    def perform_destroy(self, instance):
        instance.delete()    
