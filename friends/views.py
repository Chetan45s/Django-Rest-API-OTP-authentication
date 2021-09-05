from django.shortcuts import render
from rest_framework import generics
from friends.serializers import AuthorSerializer
from friends.models import Author
from All_Users.models import User,Profile
from All_Users.serializer import ProfilePrivateSerializers,ProfileSerializers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status 
import json

class AuthorCreateApi(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AuthorUpdateApi(generics.UpdateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

# def phone_data(profile,user_id):
#     current_user = User.objects.get(id = user_id)
#     phone = current_user.get_phone()


class AllPeoplesApi(APIView):

    def get(self,request):
        # current_user = User.objects.get(id = self.request.user.id)
        # phone = current_user.get_phone()
        # query_set = Profile.objects.filter(Phone=phone)
        # serializer =  AllPeoplesSerializer(query_set, many=True)
        all_peoples_list = []
        user_objects = User.objects.filter(staff=False,admin=False)
        for peoples in user_objects:
            if peoples.id != self.request.user.id:
                all_peoples_list.append(peoples.id)
        ava_people = {}
        ava_people['user_id'] = all_peoples_list
        ava_people_json = json.dumps(ava_people)

        return Response(ava_people_json)


# class Send_request(APIView):
    
#     def get(self,request,*args, **kwargs):
#         user_id = kwargs.get("id")



class user_data(APIView):

    def get(self,request,*args, **kwargs):
        user_id = kwargs.get("id")
        current_user = User.objects.get(id = user_id)
        phone = current_user.get_phone()
        query_set = Profile.objects.filter(Phone=phone)
        user_query_set = Profile.objects.get(Phone=phone)
        
        if user_query_set.is_private:
            serializer = ProfilePrivateSerializers(query_set,many=True)
        else:
            serializer = ProfileSerializers(query_set,many=True)

        return Response(serializer.data)