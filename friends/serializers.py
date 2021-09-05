from django.db.models import fields
from All_Users.models import Profile
from rest_framework import serializers
from friends.models import Author
from All_Users.models import Profile,User


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = (
            'name',
            'book',
            'is_valid',
        )

# class AllPeoplesSerializer(serializers.ModelSerializer):

#     AllPeoples = serializers.SerializerMethodField()

#     class Meta:

#         model = Profile
#         fields = (
#             'AllPeoples',
#         )

#     def get_AllPeoples(self, obj):
#         all_peoples_list = []
#         for peoples in User:
#             if peoples.id != self.request.user.id and peoples.is_admin() == False:
#                 all_peoples_list.append(peoples.id)
#         return all_peoples_list