import re
from All_Users.otp import generate_otp, update_otp, get_otp
from django.shortcuts import render, get_object_or_404,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,generics
from All_Users.models import User,Profile
from All_Users.serializer import RegisterSerializer,LoginUserSerializer, ProfileSerializers, ProfilePrivateSerializers

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from django.contrib.auth import get_user_model, login
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from rest_framework import status 


#File imports
from friends.views import geUserModel,printStatement

class send_otp(APIView):
    def post(self, request):

        phone = request.data.get('Phone',None)
        print(phone)
        if phone is not None:
            flag = bool(re.match('[\d]{10}', phone))
        else:
            flag = False

        if flag:
            if User.objects.filter(Phone=phone).exists():
                return Response({'message':"Phone Number is already Registered"},status=status.HTTP_400_BAD_REQUEST)

            get_otp = generate_otp(phone)

            if get_otp == '-1':
                return Response({'message': "Failed to send OTP"},status=status.HTTP_400_BAD_REQUEST)
            else:
                if Profile.objects.filter(Phone=phone).exists():
                    prof_object = Profile.objects.get(Phone=phone)
                    if prof_object.is_validate:
                        return Response({'message':'Phone Number is already Validated'},status=status.HTTP_200_OK)
                    else:
                        prof_object.otp = get_otp
                        prof_object.save()
                        return Response({'message':'OTP send Successfully'},status=status.HTTP_200_OK)
                else:
                    Profile.objects.create(Phone=phone,otp=get_otp)
                    return Response({'message':'OTP send Successfully'},status=status.HTTP_200_OK)
        else:
            return Response({'message':"Invalid Phone Number"},status=status.HTTP_400_BAD_REQUEST)

class verify_user(APIView):

    def post(self, request):

        phone = request.data.get('Phone',None)
        otp = request.data.get('otp',None)

        if phone and otp:
            flag = bool(re.match('[\d]{10}', phone)) and bool(re.match('[\d]{6}', otp))
        else:
            flag = False

        
        if flag:

            if User.objects.filter(Phone=phone).exists():
                return Response({'message':"Phone Number is already Registered"},status=status.HTTP_400_BAD_REQUEST)
            elif Profile.objects.filter(Phone=phone).exists():
                prof_obj = Profile.objects.get(Phone__iexact=phone)
                otp_obj = get_otp(phone, otp)

                if not otp_obj:
                    return Response({'message':"OTP is not matched or Time limit exceed"},status=status.HTTP_400_BAD_REQUEST)

                prof_obj.is_validate = True                
                prof_obj.save()
                return Response({'message':"OTP matched"},status=status.HTTP_200_OK)
            else:
                return Response({'message':"No Record of Phone"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':"Invalid Data"},status=status.HTTP_400_BAD_REQUEST)

class Register(APIView):

    def post(self,request,*args, **kwargs):
        phone = request.data.get('Phone',None)
        first = request.data.get('first',None)
        last = request.data.get('last',None)
        password = request.data.get('pass',None)

        if first is None:
            return Response({'message': "First Name is not Provided"},status=status.HTTP_400_BAD_REQUEST)
        
        if last is None:
            return Response({'message': "Last Name is not Provided"},status=status.HTTP_400_BAD_REQUEST)

        if phone is None:
            return Response({'message': "Phone is not Provided"},status=status.HTTP_400_BAD_REQUEST)
        
        if password is None:
            return Response({'message': "Password is not Provided"},status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(Phone=phone).exists():
            return Response({'message':"Phone Number is already Registered"},status=status.HTTP_400_BAD_REQUEST)
        elif Profile.objects.filter(Phone=phone).exists():
            prof_obj = Profile.objects.get(Phone__iexact=phone)
            if prof_obj.is_validate:
                temp_data = {
                    'Phone':phone,
                    'password':password,
                    'First_Name':first,
                    'Last_Name':last,
                }
                serializer = RegisterSerializer(data = temp_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                prof_obj.First_Name = first
                prof_obj.Last_Name = last
                prof_obj.save()
            return Response({'message':"User Registered"},status=status.HTTP_200_OK)
        else:
            return Response({'message':"No Record of Phone"},status=status.HTTP_400_BAD_REQUEST)

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']            
        login(request, user)
        return super().post(request, format=None)

# class ProfileApiView(generics.ListAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = ProfileSerializers

#     def get_queryset(self):

#         cur_user_id = geUserModel(self.request.user.id).id
#         return Profile.objects.filter(id=cur_user_id)

# class ProfileUpdateApiView(generics.UpdateAPIView):
#     permission_classes = (IsAuthenticated,)

#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializers

# class ProfilePartialUpdateView(GenericAPIView, UpdateModelMixin):

#     serializer_class = ProfileSerializers   
#     queryset = Profile.objects.all()

#     def put(self, request, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)

class ProfileApiView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializers

    def get_queryset(self):
        cur_user_id = geUserModel(self.request.user.id).id
        return Profile.objects.get(id=cur_user_id)

    def get(self, request, *args, **kwargs):
        
        user_queryset = self.get_queryset()
        serializer = ProfileSerializers(user_queryset)

        return Response(serializer.data)

    # def post(self, request, *args, **kwargs):
    #     car_data = request.data

    #     new_car = Cars.objects.create(car_brand=car_data["car_brand"], car_model=car_data[
    #         "car_model"], production_year=car_data["production_year"], car_body=car_data["car_body"], engine_type=car_data["engine_type"])

    #     new_car.save()

    #     serializer = CarsSerializer(new_car)

    #     return Response(serializer.data)

    # def put(self, request, *args, **kwargs):
    #     id = request.query_params["id"]
    #     car_object = Cars.objects.get(id=id)

    #     data = request.data

    #     car_object.car_brand = data["car_brand"]
    #     car_object.car_model = data["car_model"]
    #     car_object.production_year = data["production_year"]
    #     car_object.car_body = data["car_body"]
    #     car_object.engine_type = data["engine_type"]

    #     car_object.save()

    #     serializer = CarsSerializer(car_object)
    #     return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        cur_profile_id = geUserModel(self.request.user.id).id
        profile_object = Profile.objects.get(id=cur_profile_id)
        user_object = User.objects.get(id=self.request.user.id)
        data = request.data

        profile_object.First_Name = data.get("First_Name", profile_object.First_Name)
        user_object.First_Name = data.get("First_Name", profile_object.First_Name)
        profile_object.Last_Name = data.get("Last_Name", profile_object.Last_Name)
        user_object.Last_Name = data.get("Last_Name", profile_object.Last_Name)
        profile_object.video = data.get("video", profile_object.video)
        profile_object.bio = data.get("bio", profile_object.bio)
        profile_object.profile_pic = data.get("profile_pic", profile_object.profile_pic)
        profile_object.is_private = data.get("is_private", profile_object.is_private)

        profile_object.save()
        user_object.save()
        serializer = ProfileSerializers(profile_object)

        return Response(serializer.data)

class UserIDView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response({'userID': request.user.id}, status=status.HTTP_200_OK)