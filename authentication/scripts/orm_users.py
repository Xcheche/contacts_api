from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model



def run():
    #create_super_user()
    #get_users()
    get_superusers()    



# def get_users():
#     User = get_user_model()
#     users = User.objects.all()
#     for user in users:
#         print(f'Username: {user.username}, Email: {user.email}')

# def create_super_user():
#     User = get_user_model()
#     if not User.objects.filter(username='admin').exists():
#         User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')


def get_superusers():
    User = get_user_model()
    superusers = User.objects.filter(is_superuser=True)
    for superuser in superusers:
        print(f'Superuser: {superuser.username}, Email: {superuser.email} \n Status:{superuser.is_superuser} Password:{superuser.password}')