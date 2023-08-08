# #Create your views here.
# from rest_framework import status
# from rest_framework.response import Response

# from django.contrib.auth import authenticate
# from rest_framework.views import APIView
# # from rest_framework.permissions import AllowAny
# from .models import CustomUser, pro


# class CustomUserRegistrationView(generics.CreateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer

# class CustomAuthTokenView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, format=None):
#         username = request.data.get('username')
#         password = request.data.get('password')

#         user = authenticate(username=username, password=password)

#         if user is not None:
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key})
#         else:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# from django.shortcuts import render
# from django.http import HttpResponse
# from .models import CustomUser
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework import status
# from .models import store_user_token


# class UserLogin(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         try:
#             user = CustomUser.objects.get(username=username)
#             if user.password == password:
#                 tokens, token_user = self.gettoken(user)
#                 user.save()
#                 return HttpResponse("Success")
#             else:
#                 return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#         except CustomUser.DoesNotExist:
#             return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

#     def gettoken(self, user):
#         refresh = RefreshToken.for_user(user)
#         tokens = {
#                     'refresh': str(refresh),
#                     'access': str(refresh.access_token),
#                 }
#         token_user,_ = store_user_token.objects.get_or_create(user_id=user.pk)
#         token_user.token = tokens['access']
#         return tokens,token_ user

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import CustomUser, store_user_token, API
from django.contrib.auth import authenticate, login
# from .serializers import CustomUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import status

def userLogin(request):
    if request.method == 'POST':    
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:    
            # If the user exists, it will be stored in the variable user.
            user = CustomUser.objects.get(username=username)
            if user.password == password:
                refresh = RefreshToken.for_user(user)   #. These tokens will be used for authentication and authorization in subsequent requests.
                tokens = {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                token1,_ = store_user_token.objects.get_or_create(user_id=user.pk)
                token1.token = tokens['access']
                token1.role = user.role
                print(tokens)
                token1.save()
                request.session['token'] = token1.token
                if user.role == 'Admin':
                    return render(request, 'myapp/admin.html')
                elif user.role == 'User':
                    return render(request, 'myapp/user.html')
                elif user.role == 'Viewer':
                    return render(request, 'myapp/viewer.html')
                return HttpResponse("Success")
            else:
                return HttpResponse("Invalid Credentials")
        except CustomUser.DoesNotExist:
            return HttpResponse("User does not exist")
    else:
        return render(request, 'myapp/login.html')  

    #The session is a way to store data on the server associated with a particular user.  







# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def add_user(request):
#     if request.method == 'POST':
#         serializer = CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({'message': 'User created successfully.'}, status=201)
#         return Response(serializer.errors, status=400)


def add_user(request):
    #retrieves the 'token' value from the session data 
    token = request.session.get('token')   
    token = AccessToken(token)   #decoding the token from where will get the user_id
    userid = token['user_id']
    user, _ = CustomUser.objects.get_or_create(id=userid)
    userrole = user.role
    if userrole == 'Admin':
        if request.method == 'POST':
            # Getting the form data from the POST request
            username = request.POST['username']
            password = request.POST['password']
            role = request.POST['role']
            api = request.POST['api']

            apis = api.split(',')


            # check if the user already exists
            if CustomUser.objects.filter(username=username).exists():
                return render(request, 'myapp/adduser.html', {'error': 'Username already exists'})

            # Creating a new user with the provided data
            user = CustomUser.objects.create(
                username=username, password=password, role=role)
            user.apis.set(API.objects.filter(id__in=apis))
            #It sets the APIs that the new user should have access to. 
            # It does this by filtering the API model for the API IDs in the 'apis' list and 
            # setting these APIs for the new user.
            #It uses the __in lookup to filter the APIs whose IDs are in the apis list.
            
            return render(request, 'myapp/adduser.html', {'message': 'User added successfully!'})
        else:
            return render(request, 'myapp/adduser.html')
    else:
        return HttpResponse('Only admin can access the data.')


def remove_user(request):
    token = request.session.get('token')
    token = AccessToken(token)
    userid = token['user_id']
    user, _ = CustomUser.objects.get_or_create(id=userid)
    userrole = user.role
    if userrole == 'Admin':
        if request.method == 'POST':
            # Getting the form data from the POST request
            username = request.POST['username']

            try:
            # Try to get the user by the provided username
                user = CustomUser.objects.get(username=username)
                user.delete()

                return redirect('remove_user')
            except CustomUser.DoesNotExist:
            # If the user with the provided username doesn't exist
                return render(request, 'myapp/removeuser.html', {'error': 'User not found'})
        else:
            return render(request, 'myapp/removeuser.html',{'message': 'User added successfully!'})

    else:
        return HttpResponse("Only Admin can access the data.")


def update_user(request):
    token = request.session.get('token')
    token = AccessToken(token)
    userid = token['user_id']
    user, _ = CustomUser.objects.get_or_create(id=userid)
    userrole = user.role
    if userrole == 'Admin':
        if request.method == 'POST':
            try:

            # Update user data based on the form fields
                username = request.POST['username']
                role = request.POST['role']
                password = request.POST['password']
                api = request.POST['api']
                
        

                apis = api.split(',')

                user = get_object_or_404(CustomUser, username=username)
                if role != "":
                    user.role = role
                if password != "":
                    user.password = password
                if api != "":
                    user.apis.set(API.objects.filter(id__in=apis))
            # Save the updated user data to the database
                user.save()

            # Redirect to the user detail view after successful update
                return redirect('update_user')
            except CustomUser.DoesNotExist:
            # Handling the case when the user is not found
                return render(request, 'myapp/update.html', {'error': 'User not found'})
          
    # Render the update user form
        else:
            apis = API.objects.all()
            return render(request, 'myapp/update.html', {'apis': apis})

    else:
        return HttpResponse('Only admin can access the data.')


def add_api(request):
    token = request.session.get('token')
    token = AccessToken(token)
    userid = token['user_id']
    user, _ = CustomUser.objects.get_or_create(id=userid)
    userrole = user.role
    if userrole == 'Admin' or userrole == 'User':
        if request.method == 'POST':
        # Get the form data from the POST request
            name = request.POST['name']
            url = request.POST['url']
            endpoint = request.POST['endpoint']
            description = request.POST['description']

        # Add more fields as required based on your API model

        # Create the API object and save it to the database
            api = API.objects.create(
                name=name, url=url, endpoint=endpoint, description=description)

            return redirect('add_api')
        else:
            return render(request, 'myapp/addapi.html')

    else:
        return HttpResponse('Only admin or User can access the data')


def remove_api(request):
    token = request.session.get('token')
    token = AccessToken(token)
    userid = token['user_id']
    user, _ = CustomUser.objects.get_or_create(id=userid)
    userrole = user.role
    if userrole == 'Admin':
        if request.method == 'POST':
            name = request.POST['name']

            try:
                # Try to get the user by the provided username
                api = API.objects.get(name=name)

                # Delete the user
                api.delete()

                # Redirect to the user list page after user removal
                return redirect('remove_api')
            except API.DoesNotExist:
                # If the user with the provided username doesn't exist
                return render(request, 'myapp/removeapi.html', {'error': 'API not found'})

        else:
            apis = API.objects.all()
            return render(request, 'myapp/removeapi.html', {'apis': apis})

    else:
        return HttpResponse('Only admin.,401')


def update_api(request):
    token = request.session.get('token')
    token = AccessToken(token)
    userid = token['user_id']
    user, _ = CustomUser.objects.get_or_create(id=userid)
    userrole = user.role
    if userrole == 'Admin' or userrole == 'User':
        if request.method == 'POST':
            try:
        # Update the existing API object with the form data
                id = request.POST['id']
                name = request.POST['name']
                url = request.POST['url']
                endpoint = request.POST['endpoint']
                description = request.POST['description']

                api = get_object_or_404(API, pk=id) # Getting the data by using the id 
                # updating the data associated by the particular id
                api.name = name
                api.url = url
                api.endpoint = endpoint
                api.description = description
            

                api.save()
                # Redirect to the view_api page after API update
                return redirect('update_api')
            except API.DoesNotExist:
                # If the user with the provided username doesn't exist
                return render(request, 'myapp/updateapi.html', {'error': 'API not found'})


        else:
            apis = API.objects.all()
            return render(request, 'myapp/updateapi.html', {'apis': apis})
        #It will redirect to the updateapi page also it is for our knowledge about the API.objects what all fields to be taken as input.
    
    else:
        return HttpResponse('Only admin or User can access the data')
    

# def view_api(request):
#     token = request.session.get('token')
#     token = AccessToken(token)
#     userid = token['user_id']
#     # print(userid,'*'*100)

#     apis = CustomUser.objects.prefetch_related('apis')
   
#     return render(request, 'myapp/viewapi.html', {'apis': apis})

def view_api(request):
    #retrieves the 'token' value from the session data 
    token = request.session.get('token')
    token = AccessToken(token)  #decoding the token from where will get the user_id
    userid = token['user_id'] 
    user = CustomUser.objects.get(id = userid)
    print(user.role)
    if user.role == "Admin":
     user_apis = API.objects.all()
    # Create a dictionary to store the mapping of APIs to users
     return render(request, 'myapp/viewapi.html', {'apis': user_apis})
    # Fetch the CustomUser object with the given user_id and prefetch related APIs
    
    user = CustomUser.objects.filter(pk=userid).prefetch_related('apis').first()
    # Note: Use "first()" instead of indexing [0] to handle the case when the user is not found.
    
    if user is not None:    
        # Get the APIs associated with the user
        # user_apis = user.apis.all().values()
        user_apis = user.apis.all().values()

        return render(request, 'myapp/viewapi.html', {'apis': user_apis})
    else:
        # Handle the case when the user is not found (optional)
        print('else')
        return render(request, 'myapp/viewapi.html', {'apis': None})


#check if user_id exist then show only those api which are created by him
    
    


    












    
    

    


    



         

















  




   
