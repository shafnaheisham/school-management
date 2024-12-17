from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer,FeesManagementSerializer,FeePaymentSerializer,StudentSerializer,LibraryAddbookSerializer,LibraryBookLendingHistorySerializer
from .models import User,LibraryBookLendingHistory,LibraryBookRegister,Login,Student,FeesManagement,StudentFeesHistory
from django.contrib.auth import get_user_model,authenticate, login
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render, redirect
from django.contrib import messages
from .permissions import IsAdminUser,OfficeStaffPermission,IsLibrarian
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout


class UserLogoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        
        logout(request)  
        return redirect('login.html')  

class loginpageView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request,'login.html')


class CustomPagination(PageNumberPagination):
    """
    Custom pagination for fee payments.
    """
    page_size = 10  # Number of records per page
    page_size_query_param = 'page_size'
    max_page_size = 50



class UserRegistrationAPIView(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]
    pagination_class = CustomPagination

    def post(self, request):
        """
        Register a new user.
        """
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return render(request, 'userregistration.html', {
                'success_message': "User registered successfully!",
                 "user": {
                     "username": user.first_name,
                     "userid":user.user_id,
                    "password": user.password,
                    "user_type": user.user_type,
                     },
            })
        else:    
            return render(request, 'userregistration.html', {
                'error_message': "User registration failed. Please check the inputs.",
                })

    def get(self, request,**kwargs):
        user_id=request.data.get('userid')
        print(user_id)
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                print(user)
                serializer = UserRegistrationSerializer(user)
                users = User.objects.all()
                return render(request, 'staffdetails.html', {
             'users': serializer.data,})
            except:
                return render(request, 'staffdetails.html',{'message':'User Not Found'})
        # if user_name:
        #     try:
        #         user=User.objects.get(first_name=user_name)  
        #         serializer = UserRegistrationSerializer(user)
        #         return render(request, 'staffdetails.html', {
        #     'users': serializer.data,})
        #     except:
        # 
        #return render(request, 'staffdetails.html',{'message':'User Not Found'})   
        else:   
            users=User.objects.all()        
            paginator = self.pagination_class()
            paginated_data = paginator.paginate_queryset(users, request)
            serializer = UserRegistrationSerializer(paginated_data, many=True)
        
            return render(request, 'staffdetails.html', {
                'users': serializer.data,
                'pagination': paginator.get_paginated_response(serializer.data),
            })

    def delete(self, request):
        """
        Delete a user with confirmation (Admin only).
        """
        userid=request.data.get(id)
        user = User.objects.get(id=userid)

        if 'confirm' in request.data and request.data['confirm'] == 'yes':
            user.delete()
            return render(request, 'staffdetails.html', {
                'success_message': f"User {user.username} deleted successfully!",
            })
        else:
            return render(request, 'confirm_delete.html', {
                'user': user,
                'message': "Are you sure you want to delete this user?",
            })

class UserEditProfile(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]
    def get(self, request,**kwargs):
        """
        List all users (Admin only) with pagination.
        
        """
        try:
            userid=request.data.get(id)
            user = User.objects.get(id=userid)
            serializer = UserRegistrationSerializer(user)
            if serializer.is_valid():
                return render(request, 'usereditprofile.html', {
                    'user': serializer.data,
                })
        except User.DoesNotExist:
            return render(request, 'usereditprofile.html', {
                'error_message': "User not found.",
            })
    def patch(self,request):
        try:
            userid=request.data.get(id)
            user = User.objects.get(id=userid)
        except User.DoesNotExist:
            return render(request, 'usereditprofile.html', {
                'error_message': "User not found.",
            })

        if 'confirm' in request.data and request.data['confirm'] == 'yes':
            # Serialize the data to validate it before saving
            serializer = UserRegistrationSerializer(user, data=request.data, partial=True)
        
            if serializer.is_valid():
                serializer.save()  # Save the updated user details
                messages.success(request, f"User {user.username} updated successfully!")
            
                # Redirect to the user registration page with updated user details
                return redirect('userregistration', user_id=user.id)
            else:
                return render(request, 'useredit.html', {
                'error_message': "Failed to update user.",
                'form_errors': serializer.errors,
                })

        # If the confirm button is not pressed, render the edit form
        return render(request, 'useredit.html', {
        'user': user,
        })
        
class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to access this endpoint for login

    def post(self, request, *args, **kwargs):
        """
        Authenticate the user and set role in the session.
        """
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in and set session data
            login(request, user)
            request.session['role'] = user.user_type  # Assuming user_type contains 'administrator', 'office_staff', or 'librarian'

            # Redirect based on user role
            if user.user_type == "administrator":
                return render(request, 'admin.html', {'id': user.id, 'role': 'administrator'})
            elif user.user_type == "office_staff":
                return render(request, 'officestaff.html', {'id': user.id, 'role': 'office_staff'})
            elif user.user_type == "librarian":
                return render(request, 'librarian.html', {'id': user.id, 'role': 'librarian'})
            else:
                # If user_type is invalid
                return render(request, 'login.html',{"error": "Invalid user type"}, status=400)

        # Invalid credentials
        return render(request, 'login.html', {"message": "Invalid username or password"}, status=401)


class StudentAPIView(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]
    pagination_class = CustomPagination
    def get(self, request, *args, **kwargs):
        """
        Retrieve all students or a specific student by ID.
        """
        studid = self.request.query_params.get('studid', None)
        if studid:
            student = Student.objects.filter(studid=studid).first()
            if not student:
                return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        else:
            students = Student.objects.all()
            paginator = self.pagination_class()
            paginated_data = paginator.paginate_queryset(students, request)
            serializer = StudentSerializer(paginated_data, many=True)
            return render(request, 'studentdetails.html', {
                'students': serializer.data,
                'pagination': paginator.get_paginated_response(serializer.data),
                })

    def post(self, request, *args, **kwargs):
        """
        Register a new student.
        """
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            stud=serializer.save()
            return render(request, 'studentreg.html', {
                'success_message': "Student registered successfully!",
                "student": {
                    "name": stud.name,
                    "studid": stud.stud_id,
                },
            })
        return render(request, 'studentreg.html', {
                'error_message': "Student registration failed!",})

    def patch(self, request, *args, **kwargs):
        """
        Update a student's details.
        """
        studid = self.request.data.get('stud_id', None)
        if not studid:
            return render(request, 'studentreg.html', {
                'error_message': "Student id is required!",})
        student = Student.objects.filter(stud_id=studid).first()
        if not student:
            return render(request, 'studentreg.html', {
                'error_message': "Student Not Found!",})
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return render(request, 'studentreg.html', {
                'success_message': "Student data edited successfully!",})
        return render(request, 'studentreg.html', {
                'error_message': serializer.error,})

    def delete(self, request, *args, **kwargs):
        """
        Delete a student record (with reconfirmation prompt).
        """
        studid = self.request.data.get('stud_id', None)
        if not studid:
           return render(request, 'studentreg.html', {
                'error_message': "Student id is required!",})
        student = Student.objects.filter(stud_id=studid).first()
        if not student:
            return render(request, 'studentreg.html', {
                'error_message': "Student Not Found!",})

        # Confirm deletion via Django messages framework
        if 'confirm' in request.data and request.data['confirm'] == 'yes':
            student.delete()
            messages.success(request, f"Student {studid} has been deleted successfully.")
            return render(request, 'studentreg.html', {'success_message': 'Student deleted successfully.'})
        else:
            messages.warning(request, "Please confirm the deletion by sending 'confirm': 'yes' in the request.")
            return render(request,
                {'message': 'Please confirm deletion by sending "confirm": "yes".'})

class FeesManagementAPIView(APIView):
    
    def get(self, request):
        
        print('gethi')
        class_id=request.data.get('searchClass')
        print(class_id)
        if class_id :
             try:
                 fees = FeesManagement.objects.filter(class_name=class_id)
                 print(fees)
                 serializer = FeesManagementSerializer(fees)
                 return render(request,'feemangement.html',{'fees_detail':serializer.data,} )
             except FeesManagement.DoesNotExist:
                 return Response({"error": "Fees record not found"},)
        
        fees = FeesManagement.objects.all()
        print(fees)
        serializer = FeesManagementSerializer(fees, many=True)
        print(serializer.data)
        
        return render(request,'feemangement.html',{'fees_detail':serializer.data} )

    def post(self, request):
        print('posthi')
        
        """
        Create a new FeesManagement record.
        """
        print("POST request received:", request.data)
        serializer = FeesManagementSerializer(data=request.data)
        if serializer.is_valid():
            
            serializer.save()
            print(serializer.data)
            class_name=serializer.data['class_name']
            return  render(request,'feemangement.html',{'fees_detail':serializer.data,'message':'Fee details for {class_name} added successfully'} )
        return render(request,'feemangement.html',{'message':'Invalid data provided',} )
    
    def delete(self, request, pk):
        """
        Delete a FeesManagement record.
        """
        try:
            fees = FeesManagement.objects.get(pk=pk)
            fees.delete()
            return render(request,'feemangement.html',{"message": "Fees record deleted successfully"}, )
        except FeesManagement.DoesNotExist:
            return render(request,'feemangement.html',{"message": "Fees record not found"},)

class FeePaymentAPIView(APIView):
    """
    API view for managing fee payments with pagination.
    """
    permission_classes = [ authenticate,IsAdminUser,OfficeStaffPermission]
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        print('hi')
        fee_payments = StudentFeesHistory.objects.all()
        print(fee_payments)
        paginator = CustomPagination()
        paginated_data = paginator.paginate_queryset(fee_payments, request)
        serializer = FeePaymentSerializer(paginated_data, many=True)
        
        return render(request, 'studentfeepayment.html', {
                'feerecord': serializer.data,
                'pagination': paginator.get_paginated_response(serializer.data),
                })
            
    def post(self, request, *args, **kwargs):
       
        serializer = FeePaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return render(request,'studentfeepayment.html', {'message': "Fee payment record created successfully."})
           
        messages.error(request, "Failed to create fee payment record.")
        return render(request, 'studentfeepayment.html', {'error':'Invalid Data Provided','error_details':serializer.errors},)

    def patch(self, request, *args, **kwargs):
        """
        Update a fee payment record partially.
        """
        fee_payment_id = kwargs.get('pk')
        try:
            fee_payment = StudentFeesHistory.objects.get(pk=fee_payment_id)
            serializer = FeePaymentSerializer(fee_payment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                messages.success(request, "Fee payment record updated successfully.")
                return render(request, 'studentfeepayment.html',{'feerecord':serializer.data})
            messages.error(request, "Failed to update fee payment record.")
            return render(request, 'studentfeepayment.html',{'error_message':serializer.errors} )
        except StudentFeesHistory.DoesNotExist:
            messages.error(request, "Fee payment record not found.")
            return render(request, 'studentfeepayment.html',{"error": "Fee payment record not found."}, )

    def delete(self, request, *args, **kwargs):
        """
        Delete a fee payment record with confirmation.
        """
        fee_payment_id = kwargs.get('pk')
        try:
            fee_payment = StudentFeesHistory.objects.get(pk=fee_payment_id)

            # Check for confirmation
            confirm = request.data.get('confirm')
            if confirm == 'yes':
                fee_payment.delete()
                messages.success(request, "Fee payment record deleted successfully.")
                return render(request, 'studentfeepayment.html',{"message": "Fee payment record deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
            else:
                messages.warning(request, "Deletion action was not confirmed.")
                return render(request, 'studentfeepayment.html',{"warning": "Deletion action was not confirmed."}, status=status.HTTP_400_BAD_REQUEST)

        except StudentFeesHistory.DoesNotExist:
            messages.error(request, "Fee payment record not found.")
            return render(request, 'studentfeepayment.html',{"error": "Fee payment record not found."}, status=status.HTTP_404_NOT_FOUND)



class StudentDetailAPIView(APIView):
    """
    API view to retrieve student details for office staff and librarian.
    """
    permission_classes = [IsAuthenticated,IsAdminUser]

    def get(self, request, *args, **kwargs):
        """
        Retrieve student details by ID or fetch all students.
        """
        student_id = kwargs.get('pk')
        if student_id:
            try:
                student = Student.objects.get(pk=student_id)
                studserializer = StudentSerializer(student)
                return  render(request, 'student_details.html', {'students': studserializer.data})
            except Student.DoesNotExist:
                return render(request,{"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            students = Student.objects.all()
            studserializer = StudentSerializer(students, many=True)
            return render(request, 'student_details.html', {'students': studserializer.data})

class LibraryBookAPIView(APIView):
    permission_classes = [IsAuthenticated, IsLibrarian]
    def get(self, request):
        """
        Retrieve all library books.
        """
        print('hi')
        books = LibraryBookRegister.objects.all()
        print(books)
        serializer =LibraryAddbookSerializer (books, many=True)
        
        return render(request, 'library-books.html', {'books': serializer.data})

    def post(self, request, *args, **kwargs):
        print('hii')
        serializer = LibraryAddbookSerializer(data=request.data)
        if serializer.is_valid():
            
            serializer.save()
            return render(request, 'library-books.html', {
                'books': serializer.data,
                'message': "Book added successfully!"
            })
        else:
            books = LibraryBookRegister.objects.all()
            serializer =LibraryAddbookSerializer (books, many=True)
            return render(request, 'library-books.html', {
                'books': serializer.data,
                'message': "Failed to add the book. Please check the form inputs.",
            })
    def delete(self, request):
        """
        Delete a FeesManagement record.
        """
        print('hib')
        bookid=request.data.get('book_id')
        print(bookid)
        try:
            book = FeesManagement.objects.filter(book_id=bookid)
            book.delete()
            print(book)
            return render(request,'library-books.html',{"message": "Book record deleted successfully"}, )
        except FeesManagement.DoesNotExist:
            return render(request,'library-books.html',{"message": "Book record not found"},)    
                

class LibraryBookLendingAPIView(APIView):
    permission_classes = [IsAuthenticated, IsLibrarian]
    def get(self, request):
        """
        Retrieve all book lending records.
        """
        lendings = LibraryBookLendingHistory.objects.all()
        serializer = LibraryBookLendingHistorySerializer(lendings, many=True)
        return render(request,'library-history.html',{'history':serializer.data}, )
    def post(self, request):
        """
        Issue a book to a student.
        """
        print(request.data)
        serializer = LibraryBookLendingHistorySerializer(data=request.data)
        if serializer.is_valid():
            book_id = serializer.validated_data['book_id']
            student_id = serializer.validated_data['stud_id']
            

            # Check if the book is already issued to another student
            existing_lending = LibraryBookLendingHistory.objects.filter(
                book_id=book_id, status="Not Returned").first()
            if existing_lending:
                return render(request, 'library-lendbooks.html',
                    {"error": "Book is already issued to another student."},)
            serializer.save()
            return render(request, 'library-lendbooks.html',
                {"message": "Book issued successfully!", "data": serializer.data},)
        return render(request, 'library-lendbooks.html',
            {"error": "Invalid data provided.", "details": serializer.errors},
            )            
        
class LibraryReviewAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser,OfficeStaffPermission]
    
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        studid = self.request.query_params.get('stud_id', None)
        if studid:
            student_books = LibraryBookLendingHistory.objects.filter(stud_id=studid).first()
            if not student_books:
                return render(request,'view-library.html',{'error': 'Student not found.'}, )
            serializer = LibraryBookLendingHistorySerializer(student_books)
            return render(request, 'view-library.html', {
                'history': serializer.data,})
        else:
            lendinghistory = LibraryBookLendingHistory.objects.all()
            paginator = self.pagination_class()
            paginated_data = paginator.paginate_queryset(lendinghistory, request)
            serializer = LibraryBookLendingHistorySerializer(paginated_data, many=True)
            return render(request, 'view-library.html', {
                'history': serializer.data,
                'pagination': paginator.get_paginated_response(serializer.data),})
        # return render(request,'library-history.html',
    
        #     {"error_message": "Invalid data provided.", "details": serializer.errors})  
    
    
class ViewStudentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated,IsLibrarian]
    pagination_class = CustomPagination
    def get(self, request, *args, **kwargs):
        """
        Retrieve all students or a specific student by ID.
        """
        studid = request.data.get('student_id', None)
        if studid:
            student = Student.objects.filter(student_id=studid).first()
            if not student:
                return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        
        students = Student.objects.all()
        paginator = self.pagination_class()
        paginated_data = paginator.paginate_queryset(students, request)
        serializer = StudentSerializer(paginated_data, many=True)
        return render(request, 'library-studentdetails.html', {
                'students': serializer.data,
                'pagination': paginator.get_paginated_response(serializer.data),
                })
class ViewStudentDetailAPIViewooficestaff(APIView):
    #permission_classes = [IsAuthenticated,OfficeStaffPermission]
    pagination_class = CustomPagination
    def get(self, request, *args, **kwargs):
        """
        Retrieve all students or a specific student by ID.
        """
        studid = request.data.get('studid', None)
        if studid:
            student = Student.objects.filter(student_id=studid).first()
            if not student:
                return render(request,'viewstuddetails-officestaf.html',{'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        
        students = Student.objects.all()
        paginator = self.pagination_class()
        paginated_data = paginator.paginate_queryset(students, request)
        serializer = StudentSerializer(paginated_data, many=True)
        return render(request, 'viewstuddetails-officestaf.html', {
                'students': serializer.data,
                'pagination': paginator.get_paginated_response(serializer.data),
                })
                