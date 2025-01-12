from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from django.http import Http404, JsonResponse
from .models import get_db
# from bson import ObjectId  # For handling MongoDB ObjectIds
# from rest_framework import status
from .serializers import QuestionnaireSerializer
from datetime import datetime

# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.http import JsonResponse
from django.shortcuts import render, redirect
from bson import ObjectId
from .forms import *
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.forms import PasswordChangeForm

db = get_db()


@api_view(['POST'])
def register_user(request):
    """
    Register a new user.
    """
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            collection = db["register_user"]
            # fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
            user = serializer.save()
            # serializer.save()
            user_data = {
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "password":user.password
            }

            # Save the user data in MongoDB
            collection = db["register_user"]
            result = collection.insert_one(user_data)
            data = {"message": "User successfully registered", 
                    "status": "SUCCESS",
                    "id": str(result.inserted_id),}
        else:
            data = {
                "message": "Invalid input data",
                "status": "FAILED",
                "errors": serializer.errors,
            }
    except Exception as e:
        print("Error while registering user:", e)
        data = {"message": "Something went wrong during registration", "status": "FAILED"}

    return Response(data)


@api_view(['POST'])
def login_user(request):
    """
    Log in the user using username and password.
    """
    try:
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Creates session
            data = {"message": "You are logged in", "status": "SUCCESS"}
        else:
            data = {"message": "Invalid username or password", "status": "FAILED"}
    except Exception as e:
        print("Error during login:", e)
        data = {"message": "Something went wrong during login", "status": "FAILED"}

    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    Log out the authenticated user.
    """
    try:
        logout(request)  # Destroys session
        data = {"message": "You are logged out", "status": "SUCCESS"}
    except Exception as e:
        print("Error during logout:", e)
        data = {"message": "Something went wrong during logout", "status": "FAILED"}

    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Change the password of the authenticated user.
    """
    try:
        form = PasswordChangeForm(data=request.data, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Keeps the user logged in
            data = {"message": "Password updated successfully", "status": "SUCCESS"}
        else:
            data = {
                "message": "Invalid input data",
                "status": "FAILED",
                "errors": form.errors,
            }
    except Exception as e:
        print("Error during password change:", e)
        data = {"message": "Something went wrong during password change", "status": "FAILED"}

    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_person(request):
    """
    Add a new person.
    """
    try:
        form = AddPersonForm(request.data)

        if form.is_valid():
            collection = db["person"]  # MongoDB collection
            person_data = {
                "name": form.cleaned_data["name"],
                "email": form.cleaned_data["email"],
            }
            result = collection.insert_one(person_data)
            data = {
                "message": "Person added successfully",
                "status": "SUCCESS",
                "id": str(result.inserted_id),
            }
        else:
            data = {
                "message": "Invalid input data",
                "status": "FAILED",
                "errors": form.errors,
            }
    except Exception as e:
        print("Error while adding person:", e)
        data = {"message": "Something went wrong while adding person", "status": "FAILED"}

    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_person(request):
    """
    Retrieve persons from the database.
    """
    try:
        collection = db["person"]
        person_data = list(
            collection.find({}, {"_id": 1, "name": 1, "email": 1})
        )
        for person in person_data:
            person["_id"] = str(person["_id"])
        data = {
            "message": "Persons retrieved successfully",
            "status": "SUCCESS",
            "persons": person_data,
        }
    except Exception as e:
        print("Error while fetching persons:", e)
        data = {"message": "Something went wrong", "status": "FAILED"}

    return Response(data)



#Submit_feedback
@api_view(['GET', 'POST'])
def submit_feedback(request):
    if request.method == 'GET':
        try:
            feedbacks = list(
                db.feedback.find({}, {
                    "_id": 0,
                    "first_name_feed_supp": 1,
                    "last_name_feed_supp": 1,
                    "email_feed_supp": 1,
                    "contact_number_feed_supp": 1
                })
            )
            data = {"message": "Feedbacks retrieved successfully.", "status": "SUCCESS", "feedbacks": feedbacks}
        except Exception as e:
            print("Failed to fetch feedbacks, Error Code: SFBK000o01", e)
            data = {"message": "Something went wrong, Error Code: SFBK000o01", "status": "FAILED"}
        return Response(data)

    elif request.method == 'POST':
        try:
            serializer = FeedbackSerializer(data=request.data)
            if serializer.is_valid():
                db.feedback.insert_one(serializer.validated_data)
                data = {"message": "Feedback submitted successfully.", "status": "SUCCESS"}
            else:
                print("Failed to submit feedback, serializer errors:", serializer.errors)
                data = {"message": "Invalid input data, Error Code: SFBK000o02", "status": "FAILED"}
        except Exception as e:
            print("Failed to submit feedback, Error Code: SFBK000o03", e)
            data = {"message": "Something went wrong, Error Code: SFBK000o03", "status": "FAILED"}
        return Response(data)
#Email_support
@api_view(['POST', 'GET'])
def email_support(request):
    if request.method == "POST":
        try:
            serializer = EmailSupportSerializer(data=request.data)
            if serializer.is_valid():
                db.email_support.insert_one(serializer.validated_data)
                return Response({"message": "Support email submitted successfully.", "status": "SUCCESS"}, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            print("Failed to submit support email, Error Code: SESK000o01", e)
            return Response({"message": "Something went wrong, Error Code: SESK000o01", "status": "FAILED"}, status=500)

    elif request.method == "GET":
        try:
            email_supports = list(
                db.email_support.find({}, {"_id": 0, "first_name_feed_supp": 1, "last_name_feed_supp": 1, "email_feed_supp": 1, "contact_number_feed_supp": 1})
            )
            return Response({"message": "Support emails retrieved successfully.", "status": "SUCCESS", "email_supports": email_supports})
        except Exception as e:
            print("Failed to fetch support emails, Error Code: SESK000o02", e)
            return Response({"message": "Something went wrong, Error Code: SESK000o02", "status": "FAILED"}, status=500)
#contact_VRM
@api_view(['POST', 'GET'])
def contact_vrm(request):
    if request.method == "POST":
        try:
            serializer = ContactVRMSerializer(data=request.data)
            if serializer.is_valid():
                db.contact_vrm.insert_one(serializer.validated_data)
                return Response({"message": "Contact VRM request submitted successfully.", "status": "SUCCESS"}, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            print("Failed to submit contact VRM request, Error Code: CVRK000o01", e)
            return Response({"message": "Something went wrong, Error Code: CVRK000o01", "status": "FAILED"}, status=500)

    elif request.method == "GET":
        try:
            contact_vrms = list(
                db.contact_vrm.find({}, {"_id": 0, "first_name_feed_supp": 1, "last_name_feed_supp": 1, "email_feed_supp": 1, "contact_number_feed_supp": 1, "select_user": 1})
            )
            return Response({"message": "Contact VRM requests retrieved successfully.", "status": "SUCCESS", "contact_vrms": contact_vrms})
        except Exception as e:
            print("Failed to fetch contact VRM requests, Error Code: CVRK000o02", e)
            return Response({"message": "Something went wrong, Error Code: CVRK000o02", "status": "FAILED"}, status=500)
#ask_the_expert
@api_view(['POST', 'GET'])
def ask_the_expert(request):
    if request.method == "POST":
        try:
            serializer = AskTheExpertSerializer(data=request.data)
            if serializer.is_valid():
                db.ask_the_expert.insert_one(serializer.validated_data)
                return Response({"message": "Expert request submitted successfully.", "status": "SUCCESS"}, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            print("Failed to submit expert request, Error Code: ATEK000o01", e)
            return Response({"message": "Something went wrong, Error Code: ATEK000o01", "status": "FAILED"}, status=500)

    elif request.method == "GET":
        try:
            expert_requests = list(
                db.ask_the_expert.find({}, {"_id": 0, "first_name_exp_feed_supp": 1, "last_name_exp_feed_supp": 1, "email_exp_feed_supp": 1, "contact_number_exp_feed_supp": 1, "sla_exp_feed_supp": 1})
            )
            return Response({"message": "Expert requests retrieved successfully.", "status": "SUCCESS", "expert_requests": expert_requests})
        except Exception as e:
            print("Failed to fetch expert requests, Error Code: ATEK000o02", e)
            return Response({"message": "Something went wrong, Error Code: ATEK000o02", "status": "FAILED"}, status=500)
#  Role Management
@api_view(['POST', 'GET'])
def role_mgnt(request):
    if request.method == 'POST':
        try:
            serializer = RoleMgntSerializer(data=request.data)
            if serializer.is_valid():
                db.role_mgnt.insert_one(serializer.validated_data)
                return Response({"message": "Role successfully created.", "status": "SUCCESS"}, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            print("Failed to create role, Error Code: RMK000o01", e)
            return Response({"message": "Something went wrong, Error Code: RMK000o01", "status": "FAILED"}, status=500)
    
    elif request.method == 'GET':
        try:
            roles = list(
                db.role_mgnt.find({}, {"_id": 0, "role_name": 1, "capabilities": 1})
            )
            return Response({"message": "Roles retrieved successfully.", "status": "SUCCESS", "roles": roles})
        except Exception as e:
            print("Failed to fetch roles, Error Code: RMK000o02", e)
            return Response({"message": "Something went wrong, Error Code: RMK000o02", "status": "FAILED"}, status=500)

#  Edit Users
@api_view(['POST', 'GET'])
def edit_users(request):
    if request.method == 'POST':
        try:
            serializer = EditUsersSerializer(data=request.data)
            if serializer.is_valid():
                db.edit_users.insert_one(serializer.validated_data)
                return Response({"message": "User successfully updated.", "status": "SUCCESS"}, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            print("Failed to update user, Error Code: EUSK000o01", e)
            return Response({"message": "Something went wrong, Error Code: EUSK000o01", "status": "FAILED"}, status=500)
    
    elif request.method == 'GET':
        try:
            users = list(
                db.edit_users.find({}, {"_id": 0, "cin_no": 1, "user_name": 1, "first_name": 1, "last_name": 1, "email": 1, "company_name": 1, "phone": 1, "company_website": 1, "selected_role": 1, "capabilities": 1})
            )
            return Response({"message": "Users retrieved successfully.", "status": "SUCCESS", "users": users})
        except Exception as e:
            print("Failed to fetch users, Error Code: EUSK000o02", e)
            return Response({"message": "Something went wrong, Error Code: EUSK000o02", "status": "FAILED"}, status=500)

#  Evidence Tracker
@api_view(['POST', 'GET'])
def evidence_tracker(request):
    if request.method == 'POST':
        try:
            serializer = EvidenceTrackerSerializer(data=request.data)
            if serializer.is_valid():
                db.evidence_tracker.insert_one(serializer.validated_data)
                return Response({"message": "Evidence status updated successfully.", "status": "SUCCESS"}, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            print("Failed to update evidence status, Error Code: ETSK000o01", e)
            return Response({"message": "Something went wrong, Error Code: ETSK000o01", "status": "FAILED"}, status=500)

    elif request.method == 'GET':
        try:
            evidence = list(
                db.evidence_tracker.find({}, {"_id": 0, "rejected": 1, "pending": 1, "uploaded": 1, "inprogress": 1, "completed": 1, "total": 1, "number_evidence": 1, "number_comments": 1, "evidence_list": 1, "evi_status": 1})
            )
            return Response({"message": "Evidence details retrieved successfully.", "status": "SUCCESS", "evidence": evidence})
        except Exception as e:
            print("Failed to fetch evidence details, Error Code: ETSK000o02", e)
            return Response({"message": "Something went wrong, Error Code: ETSK000o02", "status": "FAILED"}, status=500)

#  Third Party Users
@api_view(['POST', 'GET'])
def third_party_users(request):
    if request.method == 'POST':
        try:
            serializer = ThirdPartyUsersSerializer(data=request.data)
            if serializer.is_valid():
                db.third_party_users.insert_one(serializer.validated_data)
                return Response({"message": "Third-party request resent successfully.", "status": "SUCCESS"}, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            print("Failed to resend third-party request, Error Code: TPUSK000o01", e)
            return Response({"message": "Something went wrong, Error Code: TPUSK000o01", "status": "FAILED"}, status=500)

    elif request.method == 'GET':
        try:
            third_party = list(
                db.third_party_users.find({}, {"_id": 0, "search_email": 1, "search_company_name": 1, "search_company_website": 1, "from_date": 1, "third_party_id": 1, "user_name": 1, "email": 1, "company_name": 1, "company_website": 1, "phone_number": 1, "framework_questionnaire": 1, "description": 1, "category": 1, "third_party_type": 1, "status": 1, "note": 1, "resend_questionnaire": 1})
            )
            return Response({"message": "Third-party users retrieved successfully.", "status": "SUCCESS", "third_party": third_party})
        except Exception as e:
            print("Failed to fetch third-party users, Error Code: TPUSK000o02", e)
            return Response({"message": "Something went wrong, Error Code: TPUSK000o02", "status": "FAILED"}, status=500)



# ================= Start Questionnaire API's ==============================

# POST API: Create a Questionnaire
import datetime
@api_view(['POST', 'GET', 'PUT', 'DELETE'])
def manage_questionnaire(request, pk=None):
    
    collection = db["questionnaires"]

    # POST: Create a new questionnaire
    if request.method == "POST":
        serializer = QuestionnaireSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Prepare and save data
                data = serializer.validated_data
                data["start_date"] = data["start_date"].isoformat()
                if "end_date" in data and data["end_date"]:
                    data["end_date"] = data["end_date"].isoformat()
                data["created"] = datetime.datetime.now()
                data["modified"] = datetime.datetime.now()

                result = collection.insert_one(data)
                return Response(
                    {
                        "message": "Questionnaire created successfully",
                        "id": str(result.inserted_id),
                    },
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response(
                    {"error": "Failed to save questionnaire.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET: Retrieve all questionnaires or a specific one by ID
    elif request.method == "GET":
        if pk:
            # Retrieve a specific questionnaire
            try:
                questionnaire = collection.find_one({"_id": ObjectId(pk)})
                if questionnaire:
                    questionnaire["_id"] = str(questionnaire["_id"])
                    return Response(questionnaire, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"error": "Questionnaire not found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
            except Exception as e:
                return Response(
                    {"error": "Failed to retrieve questionnaire.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            # Retrieve all questionnaires
            try:
                questionnaires = list(
                    collection.find(
                        {},
                        {
                            "_id": 1,
                            "name": 1,
                            "start_date": 1,
                            "end_date": 1,
                            "comments": 1,
                            "status": 1,
                            "created": 1,
                        },
                    )
                )
                for q in questionnaires:
                    q["_id"] = str(q["_id"])
                return Response(questionnaires, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"error": "Failed to retrieve questionnaires.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

    # PUT: Update a questionnaire by ID
    elif request.method == "PUT":
        if not pk:
            return Response(
                {"error": "ID is required for update"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = QuestionnaireSerializer(data=request.data)
        if serializer.is_valid():
            try:
                object_id = ObjectId(pk)
                updated_data = serializer.validated_data
                for key, value in updated_data.items():
                    if isinstance(value, datetime.date):
                        updated_data[key] = datetime.datetime.combine(
                            value, datetime.datetime.min.time()
                        )
                updated_data["modified"] = datetime.datetime.now()
                result = collection.update_one({"_id": object_id}, {"$set": updated_data})
                if result.matched_count:
                    return Response(
                        {"message": "Questionnaire updated successfully"},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"error": "Questionnaire not found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
            except Exception as e:
                return Response(
                    {"error": "Failed to update questionnaire.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE: Delete a questionnaire by ID
    elif request.method == "DELETE":
        if not pk:
            return Response(
                {"error": "ID is required for deletion"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            result = collection.delete_one({"_id": ObjectId(pk)})
            if result.deleted_count:
                return Response(
                    {"message": "Questionnaire deleted successfully"},
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                return Response(
                    {"error": "Questionnaire not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception as e:
            return Response(
                {"error": "Failed to delete questionnaire.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    # Handle unsupported methods
    else:
        return Response(
            {"error": "Method not allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )



# ================= End Questionnaire API's ==============================
