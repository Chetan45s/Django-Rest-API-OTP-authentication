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

def printStatement(text):
    print("----------------------------------------")
    print(text)

def geUserModel(id,ofWhat = "none"):
    current_user = User.objects.get(id = id)
    if ofWhat == "User":
        return current_user
    phone = current_user.get_phone()
    query_set = Profile.objects.filter(Phone=phone) # try catch if user doesn't exists
    if query_set.exists():
        user_query_set = Profile.objects.get(Phone=phone)
        return user_query_set
    else:
        return None

class AuthorCreateApi(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AuthorUpdateApi(generics.UpdateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

# def phone_data(profile,user_id):
#     current_user = User.objects.get(id = user_id)
#     phone = current_user.get_phone()

def checkConditons(peoples,ID):
    # not friend
    # not in between of friendship
    user_id = geUserModel(peoples.id,"User")
    user_profile_friend_stack = geUserModel(ID).user.all()
    user_request_recieve_stack = geUserModel(ID).request_receive.all()
    user_request_sent_stack = geUserModel(ID).request_sent.all()
    if user_id in user_profile_friend_stack or user_id in user_request_recieve_stack or user_id in user_request_sent_stack:
        return False
    else:
        return True

class AllPeoplesApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        # current_user = User.objects.get(id = self.request.user.id)
        # phone = current_user.get_phone()
        # query_set = Profile.objects.filter(Phone=phone)
        # serializer =  AllPeoplesSerializer(query_set, many=True)
        all_peoples_list = []
        user_objects = User.objects.filter(staff=False,admin=False)
        for peoples in user_objects:
            user_data = {}
            if peoples.id != self.request.user.id and checkConditons(peoples,self.request.user.id):
                user_data['id'] = peoples.id
                user_data['name'] = peoples.get_full_name()
                image = Profile.objects.get(Phone = User.objects.get(id = peoples.id).get_phone()).profile_pic
                user_data['image'] = image.path
                all_peoples_list.append(user_data)
        ava_people = {}
        ava_people['user_id'] = all_peoples_list
        # ava_people_json = json.dumps(ava_people)

        return Response(ava_people)


class Send_request(APIView):
    
    def get(self,request,*args, **kwargs):
        user_id = kwargs.get("id")
        current_user = geUserModel(user_id)                 #getting profile model
        loggedIn_user = geUserModel(self.request.user.id)   #getting profile model


        if geUserModel(user_id,"User") in loggedIn_user.user.all():
            return Response({'message': "Already Friend"},status=status.HTTP_400_BAD_REQUEST)

        if geUserModel(user_id,"User") in loggedIn_user.request_sent.all():
            return Response({'message': "Already Requested"},status=status.HTTP_400_BAD_REQUEST)

        loggedIn_user.request_sent.add(user_id)
        current_user.request_receive.add(self.request.user.id)
        loggedIn_user.save()
        current_user.save()
        return Response({'message': "Request Sent"},status=status.HTTP_200_OK)


class Accept_request(APIView):
    
    def get(self,request,*args, **kwargs):
        user_id = kwargs.get("id")

        current_user = geUserModel(user_id)
        loggedIn_user = geUserModel(self.request.user.id)

        if geUserModel(user_id,"User") in loggedIn_user.request_receive.all() and geUserModel(self.request.user.id,"User") in current_user.request_sent.all():
            loggedIn_user.request_sent.remove(user_id)
            current_user.request_receive.remove(self.request.user.id)
            loggedIn_user.user.add(user_id)
            current_user.user.add(self.request.user.id)
            loggedIn_user.save()
            current_user.save()
            return Response({'message': "Request Accepted"},status=status.HTTP_200_OK)
        return Response({'message': "Invalid Request"},status=status.HTTP_400_BAD_REQUEST)

class Delete_request(APIView):
    
    def get(self,request,*args, **kwargs):
        user_id = kwargs.get("id")
        current_user = geUserModel(user_id)

        if geUserModel(user_id,"User") in current_user.request_receive.all():
            loggedIn_user = geUserModel(self.request.user.id)
            loggedIn_user.request_sent.remove(user_id)
            current_user.request_receive.remove(self.request.user.id)
            loggedIn_user.save()
            current_user.save()
            return Response({'message': "Request Rejected"},status=status.HTTP_200_OK)
        
        if geUserModel(user_id,"User") in geUserModel(self.request.user.id).request_sent.all():
            loggedIn_user = geUserModel(self.request.user.id)
            loggedIn_user.request_sent.remove(user_id)
            current_user.request_receive.remove(self.request.user.id)
            loggedIn_user.save()
            current_user.save()
            return Response({'message': "Request Cancelled"},status=status.HTTP_200_OK)

        return Response({'message': "Invalid Request"},status=status.HTTP_400_BAD_REQUEST)

class removeFriend(APIView):
    
    def get(self,request,*args, **kwargs):
        user_id = kwargs.get("id")
        current_user = geUserModel(user_id)
        loggedIn_user = geUserModel(self.request.user.id)

        if geUserModel(user_id,"User") in current_user.request_sent.all() or geUserModel(user_id,"User") in current_user.request_receive.all():
            return Response({'message': "Friend Status is in Middle"},status=status.HTTP_200_OK)


        if geUserModel(user_id,"User") in loggedIn_user.user.all():
            loggedIn_user.user.remove(user_id)
            current_user.user.remove(self.request.user.id)
            loggedIn_user.save()
            current_user.save()
            return Response({'message': "Friend Removed"},status=status.HTTP_200_OK)

        return Response({'message': "Invalid Request"},status=status.HTTP_400_BAD_REQUEST)

class user_data(APIView):

    def get(self,request,*args, **kwargs):
        user_id = kwargs.get("id")
        current_user = User.objects.get(id = user_id)
        phone = current_user.get_phone()
        query_set = Profile.objects.filter(Phone=phone) # try catch if user doesn't exists
        user_query_set = Profile.objects.get(Phone=phone)

        if geUserModel(user_id,"User") in geUserModel(self.request.user.id).user.all() or user_id == self.request.user.id:
            serializer = ProfileSerializers(query_set,many=True)
            return Response(serializer.data)

        
        if user_query_set.is_private:
            serializer = ProfilePrivateSerializers(query_set,many=True)
        else:
            serializer = ProfileSerializers(query_set,many=True)
        return Response(serializer.data)


class showMyFriends(APIView):
    
    def get(self,request,*args, **kwargs):
        all_peoples_list = []
        user_objects = geUserModel(self.request.user.id)
        for peoples in user_objects.user.all():
            user_data = {}
            user_data['id'] = peoples.id
            user_data['name'] = peoples.get_full_name()
            image = Profile.objects.get(Phone = User.objects.get(id = peoples.id).get_phone()).profile_pic
            user_data['image'] = image.path
            all_peoples_list.append(user_data)
        ava_people = {}
        ava_people['user_id'] = all_peoples_list

        return Response(ava_people)

class pendingRequests(APIView):

    def get(self,request,*args, **kwargs):
        all_peoples_list = []
        user_objects = geUserModel(self.request.user.id)
        for peoples in user_objects.request_sent.all():
            user_data = {}
            user_data['id'] = peoples.id
            user_data['name'] = peoples.get_full_name()
            image = Profile.objects.get(Phone = User.objects.get(id = peoples.id).get_phone()).profile_pic
            user_data['image'] = image.path
            all_peoples_list.append(user_data)
        ava_people = {}
        ava_people['user_id'] = all_peoples_list

        return Response(ava_people)

class nonResponsedRequests(APIView):
    
    def get(self,request,*args, **kwargs):
        all_peoples_list = []
        user_objects = geUserModel(self.request.user.id)
        for peoples in user_objects.request_receive.all():
            user_data = {}
            user_data['id'] = peoples.id
            user_data['name'] = peoples.get_full_name()
            image = Profile.objects.get(Phone = User.objects.get(id = peoples.id).get_phone()).profile_pic
            user_data['image'] = image.path
            all_peoples_list.append(user_data)
        ava_people = {}
        ava_people['user_id'] = all_peoples_list

        return Response(ava_people)