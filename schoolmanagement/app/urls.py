from django.urls import path
from .views import StudentAPIView,UserRegistrationAPIView,UserLoginAPIView,loginpageView,LibraryBookLendingAPIView,LibraryBookAPIView
from .views import *
urlpatterns = [
    path('',loginpageView.as_view(), name='loginpage'),

    path('login/', UserLoginAPIView.as_view(), name='login'),  # Login page
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
    
    path('login/userregistration/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('login/userregistration/userregistration/', UserRegistrationAPIView.as_view(), name='user-search'),
    path('login/userregistration/usereditprofile/', UserEditProfile.as_view(), name='usereditprofile'),
    path('login/studentregister/',StudentAPIView.as_view(),name='studentregister'),
    
    
    path('login/view-lending-history/',LibraryReviewAPIView.as_view(), name='view_lending_history'),
    path('login/addfees/',FeesManagementAPIView.as_view(),name='addfees'),
    path('login/viewstudent-details/',ViewStudentDetailAPIViewooficestaff.as_view(),name='viewstudentdetails'),
    path('login/studentfeepayment/',FeePaymentAPIView.as_view(),name='studentfeepayment'),
    
    
    path('login/library-add-books/',LibraryBookAPIView.as_view(),name='add-books'),
    path('login/editbooks/<str:book_id>/',LibraryBookAPIView.as_view(),name='editbooks'),
    path('login/issue-books/',LibraryBookLendingAPIView.as_view(),name='issue-books'),
    path('login/view-students/',ViewStudentDetailAPIView.as_view(),name='view-students'),
]