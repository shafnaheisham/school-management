from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FeesManagement,Student,User,StudentFeesHistory
from django.contrib.auth.hashers import make_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
             'user_type', 'first_name', 'last_name', 
            'email', 'phone_number', 'address', 'date_of_birth', 
             'gender','profile_picture'
        ]
        read_only_fields = ['id','username'] 
        extra_kwargs = {
            'password': {'write_only': True},
            'user_id': {'read_only': True},  # Auto-generated
            
        }

    def create(self, validated_data):
        user_type = validated_data['user_type']
        # Generate custom user_id prefix based on user type
        prefix = {
            'administrator': 'AD',
            'office_staff': 'OS',
            'teacher': 'TE',
            'librarian': 'LB',
        }.get(user_type, 'US')  # Default prefix if user type is invalid
        last_user = User.objects.filter(user_type=user_type).last()
        next_id = f"{last_user.id + 1:02d}" if last_user else "001"
        custom_user_id = f"{prefix}{next_id}"

        validated_data['username'] = custom_user_id

        # Hash the password before saving
        #validated_data['password'] = make_password(validated_data['password'])
        
        return super().create(validated_data)





class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [ 'name', 'class_name', 'division','admission_date', 'parent_contact', 'address', 'date_of_birth', 
             'gender','profile_picture']
        read_only_fields = ['stud_id'] 




class OfficeStaffPermission:
    """
    Custom permission to grant access only to office staff.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='OfficeStaff').exists()

# Serializer for FeePayment
class FeePaymentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_class = serializers.CharField(source='student.class_name', read_only=True)
    
    class Meta:
        model = StudentFeesHistory
        fields = ['student_id', 'student_name', 'student_class', 'amount', 'paid_date', 
                  'first_quarter_fee', 'second_quarter_fee', 'third_quarter_fee', 
                  'other_fees', 'remarks']
        read_only_fields = ['student_name', 'student_class']

        


class FeesManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeesManagement
        fields = '__all__'

    def validate_class_name(self, value):
        if FeesManagement.objects.filter(class_name=value).exists():
            raise serializers.ValidationError("A record for this class already exists.")
        return value

    def create(self, validated_data):
        return FeesManagement.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


from .models import LibraryBookRegister

class LibraryAddbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryBookRegister
        fields = '__all__'
        read_only_fields = ('book_id',)

    def create(self, validated_data):
        # The save method of the model will handle book_id generation.
        return LibraryBookRegister.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


from datetime import date, timedelta
from .models import LibraryBookLendingHistory

class LibraryBookLendingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryBookLendingHistory
        fields = '__all__'
        read_only_field='fine'

    def validate(self, data):
        due_date = data.get('due_date')
        if due_date and date.today() > due_date:
            days_overdue = (date.today() - due_date).days
            fine = 10  # Base fine amount
            periods_of_15_days = days_overdue // 15

            # Double the fine for every 15 days late
            total_fine = fine * (2 ** periods_of_15_days)

            data['fine'] = total_fine
        else:
            data['fine'] = 0  # No fine if returned before or on due date

        return data
