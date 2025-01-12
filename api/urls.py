# from django.urls import path
# from . import views

# urlpatterns = [
#     path('api/login/', login_user, name='login'), 
#     path('api/logout/', logout_user, name='logout'), 
#     path('api/register/', register_user, name='register'), 
#     path('api/change_password/', change_password, name='change_password'), 
#     path('api/add_person/', add_person, name='add_person'),
#       path('api/get_person/', get_person, name='get_person'),
    
    
    
#     path("submit-feedback/", views.submit_feedback, name="submit_feedback"),
#     path("email-support/", views.email_support, name="email_support"),
#     path("contact-vrm/", views.contact_vrm, name="contact_vrm"),
#     path("ask-the-expert/", views.ask_the_expert, name="ask_the_expert"),
#      # Role Management
#     path('role_mgnt/', views.role_mgnt, name='role_mgnt'),
    
#     # Edit Users
#     path('edit_users/', views.edit_users, name='edit_users'),
    
#     # Evidence Tracker
#     path('evidence_tracker/', views.evidence_tracker, name='evidence_tracker'),
    
#     # Third Party Users
#     path('third_party_users/', views.third_party_users, name='third_party_users'),
# ]

from django.urls import path
from .views import *

urlpatterns = [
    # Authentication
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register_user'),
    path('change-password/', change_password, name='change_password'),
    path('add-person/', add_person, name='add_person'),
    # Person Management
    path('add-person/', add_person, name='add_person'),
    path('get-person/', get_person, name='get_person'),
 path('logout/', logout_user, name='logout'),
    # Feedback
    path('submit-feedback/', submit_feedback, name='submit_feedback'),

    # Email Support
    path('email-support/', email_support, name='email_support'),

    # Contact VRM
    path('contact-vrm/', contact_vrm, name='contact_vrm'),

    # Ask the Expert
    path('ask-the-expert/', ask_the_expert, name='ask_the_expert'),

    # Role Management
    path('role-management/', role_mgnt, name='role_management'),

    # Edit Users
    path('edit-users/', edit_users, name='edit_users'),

    # Evidence Tracker
    path('evidence-tracker/', evidence_tracker, name='evidence_tracker'),

    # Third Party Users
    path('third-party-users/', third_party_users, name='third_party_users'),

    # Quesstionari
    path('questionnaire/', manage_questionnaire, name='create_questionnaire'),
    path('questionnaires/', manage_questionnaire, name='get_questionnaires'),
    path('questionnaire/<str:pk>/',manage_questionnaire, name='update_questionnaire'),
    path('questionnaire/delete/<str:pk>/', manage_questionnaire, name='delete_questionnaire'),
]
