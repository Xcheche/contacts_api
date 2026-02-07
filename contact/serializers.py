from rest_framework import serializers
from .models import Contact



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        #fields = '__all__'
        fields = ['id', 'first_name', 'last_name','country_code', 'phone_number']