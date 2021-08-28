import re
from All_Users.otp import generate_otp, update_otp, get_otp
from django.shortcuts import render, get_object_or_404,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from All_Users.models import User,Profile
from All_Users.serializer import RegisterSerializer,LoginUserSerializer, ProfileSerializers


from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from rest_framework import status 

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


# class ProfileView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         serialized_profile = ProfileSerializers(Profile.objects.filter(Phone=self.request.user.Phone),many=True).data
#         serialized_appointment = AllBookingSerializers(AllBooking.objects.filter(User=self.request.user),many=True).data
#         serialized_order_pending = OrderSerializers(Order.objects.filter(Patient=self.request.user,Ordered=False),many=True).data
#         serialized_order_ongoing = OrderSerializers(Order.objects.filter(Patient=self.request.user,Ordered=True,service_status="Order Placed"),many=True).data
#         serialized_order_history = OrderSerializers(Order.objects.filter(Patient=self.request.user,Ordered=True,service_status="Result Out"),many=True).data
#         final_response = {
#             'Personal Detail' : serialized_profile,
#             'Appointments' : serialized_appointment,
#             'Pending Order' : serialized_order_pending,
#             'Ordered' : serialized_order_ongoing,
#             'History' : serialized_order_history,
#         }
#         return Response(final_response)
        # return Response(serialized_profile+serialized_appointment+serialized_order_pending+serialized_order_ongoing+serialized_order_history)