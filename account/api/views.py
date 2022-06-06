from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import LoginSerializer
from django.contrib.auth import authenticate,login
import jwt
import datetime
from django.utils import timezone
from reg_org.models import Organization
import uuid
from django.core.exceptions import ValidationError
@api_view(['POST'])
def login_view(request,org):
    try:
        if Organization.objects.filter(org_name=org).exists():
            client_secret=request.META.get('HTTP_CLIENT_SECRET')
            org=Organization.objects.get(client_secret=client_secret)
            
            if org is None:
                return Response({"error":'Invalid secret Key'})  
            
            
            if request.method == 'POST':
                
                serializer=LoginSerializer(data=request.data)
                # print(serializer)
                if serializer.is_valid():
                    username=serializer.data['username']
                    password=serializer.data['password']
                    user=authenticate(username=username,password=password)
                    
                    if user is not None:
                        # as the user exist in the database , we now need to generate a jwt token 
                        # now i can decide what things i can give to encode the payload
                        encoded=jwt.encode({
                            "id":user.id,
                            "username":user.username,
                            "exp": datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(seconds=300),
                            "iat": datetime.datetime.now(tz=timezone.utc)},"secret_key",algorithm="HS256")
                        
                                        
                        data={
                            'message':'Logged in sucessfully',
                            'access_token':encoded
                        }
                        
                        return Response(data)
                        
                    else:
                        
                        data={
                            'message':'Invalid credentials'
                            
                        }
                        return Response(data)
                        
                else:
                    return Response({'error':serializer.errors})
        else:
            return Response({'error':'Invalid URL'})
    except ValidationError as v:
        return Response({'errorTE':v.__cause__})
