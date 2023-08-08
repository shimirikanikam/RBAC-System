from django.db import models

# # Role model to represent different user roles
# class Role(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.name

# # API model to represent different APIs
# class API(models.Model):
#     name = models.CharField(max_length=100)
#     url = models.CharField(max_length=200)
#     endpoint = models.CharField(max_length=100)
#     description = models.TextField()


#     def __str__(self):
#         return self.name

# # CustomUser model with custom fields and relationships
# class CustomUser(models.Model):
#     email = models.EmailField(max_length=254, unique=True)
#     mobile_no = models.CharField(max_length=15)
#     role= models.CharField(max_length=50)
    
    
#     # Provide unique related_name arguments to avoid clashes
#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='customuser_set',
#         blank=True,
#         help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
#         verbose_name='groups',
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='customuser_set',
#         blank=True,
#         help_text='Specific permissions for this user.',
#         verbose_name='user permissions',
#     )

#     def __str__(self):
#         return self.username

#  class store_user_token(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     role = models.CharField(choices=[('Admin','Admin'),('User', 'User')])



class API(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    endpoint = models.CharField(max_length=100)
    description = models.TextField()
 
#the first element is the actual value to be set on the model,and the second element is the human readable name.
class CustomUser(models.Model):
    ROLES = (
        ('Admin', 'Admin'),
        ('User', 'User'),
        ('Viewer', 'Viewer'),
    )
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=20, choices=ROLES)
    apis = models.ManyToManyField(API)

class store_user_token(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(choices=[('Admin', 'Admin'),('User', 'User'),('Viewer', 'Viewer')], max_length=10)
    token = models.CharField(max_length=750, blank=True, null=True)