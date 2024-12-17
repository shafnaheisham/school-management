from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.hashers import make_password

CLASS_CHOICES = [
        ('Nursery', 'Nursery'),
        ('KG', 'Kindergarten'),
        ('1', 'Class 1'),
        ('2', 'Class 2'),
        ('3', 'Class 3'),
        ('4','Class 4'),
        ('5','Class 5'),
        ('6','Class 6'),
        ('7','Class 8'),
        ('8','Class 8'),
        ('9','Class 9'),
        ('10','Class 10'),
        ('11','Class 11'),
        ('12','Class 12')
        # Add more classes as required
    ]
# class MyAccountManager(BaseUserManager):
#     def create_user(self, email, username, password= None):
#         if not email:
#             raise ValueError('email required')
#         if not username:
#             raise ValueError('username required')

#         user = self.model(
#             email= self.normalize_email(email),
#             username= username,
#         )
#         user.set_password(password)
#         user.save(using= self._db)
#         return user

    # def create_superuser(self, email, username, password):
    #     user = self.create_user(
    #         email= self.normalize_email(email),
    #         password= password,
    #         username= username,
    #     )
    #     user.is_admin= True
    #     user.staff= True
    #     user.is_superuser= True
    #     user.save(using= self._db)
    #     return user
class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('administrator', 'Administrator'),
        ('office_staff', 'Office Staff'),
        ('teacher', 'Teacher'),
        ('librarian', 'Librarian'),
    ]
    user_id = models.CharField(max_length=10, unique=True, editable=False, blank=True, null=True) 
    username = models.CharField(max_length=10, unique=True, editable=True, blank=False, null=False) 
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
          # Hash the password if it is not already hashed
          if self.pk is None or not self.password.startswith('pbkdf2_sha256$'):
              self.password = make_password(self.password)
          super().save(*args, **kwargs)

    def __str__(self):
        return f"Profile of {self.username} - {self.user_type}"


class Login(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    password = models.CharField(max_length=255)
   
    def __str__(self):
        return f"Login for {self.user.username}"


class Student(models.Model):
    # Auto-generated student ID
    stud_id =models.CharField(max_length=10, unique=True, editable=False) 
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    class_name = models.CharField(max_length=50, choices=CLASS_CHOICES)
    division = models.CharField(max_length=5)
    admission_date = models.DateField()
    parent_contact = models.CharField(max_length=15)
    
    def save(self, *args, **kwargs):
        if not self.stud_id:
            # Generate custom ID with prefix 'ST' and auto-increment number
            last_student = Student.objects.order_by('id').last()
            if last_student:
                new_id = int(last_student.stud_id[2:]) + 1
            else:
                new_id = 1
            self.stud_id = f"ST{new_id:03d}"  # Format as ST001, ST002, etc.
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.stud_id} - {self.name}"


class FeesManagement(models.Model):
    class_name = models.CharField(max_length=50,unique=True, choices=CLASS_CHOICES)
    first_quarter_fees = models.IntegerField()
    second_quarter_fees = models.IntegerField()
    third_quarter_fees = models.IntegerField()
    other_fees = models.IntegerField()

    class Meta:
        verbose_name = "Fees Management"
        verbose_name_plural = "Fees Management"

    def __str__(self):
        return f"{self.class_name} Fees"

class StudentFeesHistory(models.Model):
    FEE_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
    )
    # Fee fields with choices (paid/pending)
    student_id = models.ForeignKey(Student, to_field='stud_id', on_delete=models.CASCADE, related_name='fees_histories')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_date= models.DateField()
    first_quarter_fee = models.CharField(max_length=7, choices=FEE_STATUS_CHOICES, default='pending')
    second_quarter_fee = models.CharField(max_length=7, choices=FEE_STATUS_CHOICES, default='pending')
    third_quarter_fee = models.CharField(max_length=7, choices=FEE_STATUS_CHOICES, default='pending')
    other_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    remarks = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.student_id} - {self.amount}"

class LibraryBookRegister(models.Model):
    book_id = models.CharField(max_length=20, unique=True, editable=False)
    book_name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication = models.CharField(max_length=255)
    edition = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Library Book Register"
        verbose_name_plural = "Library Book Register"

    def save(self, *args, **kwargs):
        if not self.book_id:
            last_book = LibraryBookRegister.objects.order_by('-id').first()
            next_id = last_book.id + 1 if last_book else 1
            self.book_id = f'LB{next_id:05d}'  # Generates IDs like LB00001, LB00002, etc.
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.book_name} ({self.book_id})"



from datetime import date

User = get_user_model()

class LibraryBookLendingHistory(models.Model):
    
    stud_id = models.ForeignKey('Student',on_delete=models.CASCADE,null=True,blank=True,
                                related_name='book_lendings_student')
    
    book_id = models.ForeignKey('LibraryBookRegister',on_delete=models.CASCADE,related_name='book_lending_history')
    borrow_date = models.DateField()
    due_date = models.DateField()
    returned_date=models.DateField(null=True,blank=True)
    status = models.CharField(choices=[('Returned', 'Returned'), ('Not Returned', 'Not Returned')],
                              default='Not Returned',max_length=20)

    fine = models.IntegerField(default=0,null=True,blank=True)

    class Meta:
        verbose_name = "Library Book Lending History"
        verbose_name_plural = "Library Book Lending Histories"

    def save(self, *args, **kwargs):
        if self.returned_date:
            self.status='Returned'
            
        # Calculate fine if current date is greater than due date
        
            if self.due_date and self.returned_date > self.due_date:
                overdue_days = (self.returned_date - self.due_date).days
                self.fine = overdue_days * 10  # Fine is 10 per day
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Lending record for {self.book_id} ({self.stud_id})"
