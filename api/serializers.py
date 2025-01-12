# # # support/serializers.py
# # from rest_framework import serializers
# # from .models import Feedback, EmailSupport

# # # Serializer for Feedback
# # class FeedbackSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Feedback
# #         fields = ['first_name_feed_supp', 'last_name_feed_supp', 'email_feed_supp',
# #                   'contact_number_feed_supp', 'subject_line', 'details_feed_supp']

# # # Serializer for Email Support
# # class EmailSupportSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = EmailSupport
# #         fields = ['first_name_feed_supp', 'last_name_feed_supp', 'email_feed_supp',
# #                   'contact_number_feed_supp', 'subject_line', 'details_feed_supp']

from rest_framework import serializers
from django.contrib.auth.models import User
# from .models import get_db

# db = get_db()

# Serializer for User Registration
# class UserSerializer(serializers.ModelSerializer):
#     password1 = serializers.CharField(write_only=True)
#     password2 = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']

#     def validate(self, data):
#         """
#         Check that the two password entries match.
#         """
#         if data['password1'] != data['password2']:
#             raise serializers.ValidationError("Passwords must match")
#         return data

#     def create(self, validated_data):
#         """
#         Create a new user and set the password.
#         """
#         user = User(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name']
#         )
#         user.set_password(validated_data['password1'])
#         user.save()
#         return user

# # Serializer for Person (using MongoDB)
# class PersonSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=100)
#     email = serializers.EmailField()

#     def create(self, validated_data):
#         """
#         Create a new Person entry in MongoDB.
#         """
#         result = db["person"].insert_one(validated_data)
#         validated_data['id'] = str(result.inserted_id)
#         return validated_data

#     def update(self, instance, validated_data):
#         """
#         Update an existing Person entry in MongoDB.
#         """
#         db["person"].update_one({"_id": instance['_id']}, {"$set": validated_data})
#         instance.update(validated_data)
#         return instance

from rest_framework import serializers
from django.contrib.auth.models import User

# Serializer for user registration
class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def validate(self, data):
        """
        Validate that password1 and password2 match.
        """
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match"})
        return data

    def create(self, validated_data):
        # Remove password2 as it's not needed for user creation
        validated_data.pop('password2')

        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password1']  # Use password1 for user creation
        )
        return user




class FeedbackSerializer(serializers.Serializer):
    first_name_feed_supp = serializers.CharField(required=True, max_length=100)
    last_name_feed_supp = serializers.CharField(required=True, max_length=100)
    email_feed_supp = serializers.EmailField(required=True)
    contact_number_feed_supp = serializers.CharField(required=True, max_length=15)
    # subject_line = serializers.CharField(required=True, max_length=255)
    # details_feed_supp = serializers.CharField(required=True, max_length=1000)

class EmailSupportSerializer(serializers.Serializer):
    first_name_feed_supp = serializers.CharField(required=True, max_length=100)
    last_name_feed_supp = serializers.CharField(required=True, max_length=100)
    email_feed_supp = serializers.EmailField(required=True)
    contact_number_feed_supp = serializers.CharField(required=True, max_length=15)
    subject_line = serializers.CharField(required=True, max_length=255)
    details_feed_supp = serializers.CharField(required=True, max_length=1000)

class ContactVRMSerializer(serializers.Serializer):
    first_name_feed_supp = serializers.CharField(required=True, max_length=100)
    last_name_feed_supp = serializers.CharField(required=True, max_length=100)
    email_feed_supp = serializers.EmailField(required=True)
    contact_number_feed_supp = serializers.CharField(required=True, max_length=15)
    reason_type = serializers.CharField(required=True, max_length=255)
    select_user = serializers.CharField(required=True, max_length=100)
    user_details = serializers.CharField(required=True, max_length=1000)

class AskTheExpertSerializer(serializers.Serializer):
    first_name_exp_feed_supp = serializers.CharField(required=True, max_length=100)
    last_name_exp_feed_supp = serializers.CharField(required=True, max_length=100)
    email_exp_feed_supp = serializers.EmailField(required=True)
    contact_number_exp_feed_supp = serializers.CharField(required=True, max_length=15)
    sla_exp_feed_supp = serializers.CharField(required=True, max_length=255)
    details_supp = serializers.CharField(required=True, max_length=1000)

# 1. Role Management Serializer
class RoleMgntSerializer(serializers.Serializer):
    role_name = serializers.CharField(required=True, max_length=100)
    selected_role = serializers.CharField(required=True, max_length=100)
    capabilities = serializers.ListField(child=serializers.CharField(), required=True)

# 2. Edit Users Serializer
class EditUsersSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True, max_length=100)
    last_name = serializers.CharField(required=True, max_length=100)
    email = serializers.EmailField(required=True)
    company_name = serializers.CharField(required=True, max_length=255)
    phone = serializers.CharField(required=True, max_length=15)
    company_website = serializers.URLField(required=True)
    selected_role = serializers.CharField(required=True, max_length=100)
    capabilities = serializers.ListField(child=serializers.CharField(), required=True)

# 3. Evidence Tracker Serializer
class EvidenceTrackerSerializer(serializers.Serializer):
    file_input_lable = serializers.CharField(required=True, max_length=255)
    evi_status = serializers.CharField(required=True, max_length=50)

# 4. Third Party Users Serializer
class ThirdPartyUsersSerializer(serializers.Serializer):
    resend_questionnaire = serializers.BooleanField(required=True)
    search_email = serializers.EmailField(required=False)
    search_company_name = serializers.CharField(required=False, max_length=255)
    search_company_website = serializers.URLField(required=False)
    from_date = serializers.DateField(required=False)
    third_party_id = serializers.CharField(required=False, max_length=100)
    user_name = serializers.CharField(required=False, max_length=100)
    email = serializers.EmailField(required=False)
    company_name = serializers.CharField(required=False, max_length=255)
    company_website = serializers.URLField(required=False)
    phone_number = serializers.CharField(required=False, max_length=15)
    framework_questionnaire = serializers.CharField(required=False, max_length=255)
    description = serializers.CharField(required=False, max_length=1000)
    category = serializers.CharField(required=False, max_length=255)
    third_party_type = serializers.CharField(required=False, max_length=100)
    status = serializers.CharField(required=False, max_length=50)
    note = serializers.CharField(required=False, max_length=1000)

# 4.  Questionnaire Serializer
class QuestionnaireSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)  # Optional since MongoDB auto-generates it
    name = serializers.CharField(max_length=100)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(allow_null=True, required=False)
    comments = serializers.CharField(max_length=256, allow_blank=True, required=False)
    status = serializers.CharField(max_length=100, allow_blank=True, required=False)
    created = serializers.DateTimeField(required=False)
    modified = serializers.DateTimeField(required=False)
