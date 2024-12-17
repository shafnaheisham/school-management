# Generated by Django 4.2.17 on 2024-12-16 06:52

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_id', models.CharField(blank=True, editable=False, max_length=10, null=True, unique=True)),
                ('username', models.CharField(blank=True, editable=False, max_length=10, null=True, unique=True)),
                ('user_type', models.CharField(choices=[('administrator', 'Administrator'), ('office_staff', 'Office Staff'), ('teacher', 'Teacher'), ('librarian', 'Librarian')], max_length=20)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='FeesManagement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(choices=[('Nursery', 'Nursery'), ('KG', 'Kindergarten'), ('1', 'Class 1'), ('2', 'Class 2'), ('3', 'Class 3'), ('4', 'Class 4'), ('5', 'Class 5'), ('6', 'Class 6'), ('7', 'Class 8'), ('8', 'Class 8'), ('9', 'Class 9'), ('10', 'Class 10'), ('11', 'Class 11'), ('12', 'Class 12')], max_length=50)),
                ('first_quarter_fees', models.IntegerField()),
                ('second_quarter_fees', models.IntegerField()),
                ('third_quarter_fees', models.IntegerField()),
                ('other_fees', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Fees Management',
                'verbose_name_plural': 'Fees Management',
            },
        ),
        migrations.CreateModel(
            name='LibraryBookRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_id', models.CharField(editable=False, max_length=20, unique=True)),
                ('book_name', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('publication', models.CharField(max_length=255)),
                ('edition', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Library Book Register',
                'verbose_name_plural': 'Library Book Register',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stud_id', models.CharField(editable=False, max_length=10, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('class_name', models.CharField(choices=[('Nursery', 'Nursery'), ('KG', 'Kindergarten'), ('1', 'Class 1'), ('2', 'Class 2'), ('3', 'Class 3'), ('4', 'Class 4'), ('5', 'Class 5'), ('6', 'Class 6'), ('7', 'Class 8'), ('8', 'Class 8'), ('9', 'Class 9'), ('10', 'Class 10'), ('11', 'Class 11'), ('12', 'Class 12')], max_length=50)),
                ('division', models.CharField(max_length=5)),
                ('admission_date', models.DateField()),
                ('parent_contact', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='StudentFeesHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('paid_date', models.DateField()),
                ('first_quarter_fee', models.CharField(choices=[('paid', 'Paid'), ('pending', 'Pending')], default='pending', max_length=7)),
                ('second_quarter_fee', models.CharField(choices=[('paid', 'Paid'), ('pending', 'Pending')], default='pending', max_length=7)),
                ('third_quarter_fee', models.CharField(choices=[('paid', 'Paid'), ('pending', 'Pending')], default='pending', max_length=7)),
                ('other_fees', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fees_histories', to='app.student', to_field='stud_id')),
            ],
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LibraryBookLendingHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrow_date', models.DateField()),
                ('due_date', models.DateField()),
                ('returned_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Returned', 'Returned'), ('Not Returned', 'Not Returned')], default='Not Returned', max_length=20)),
                ('fine', models.IntegerField(default=0)),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_lending_history', to='app.librarybookregister')),
                ('stud_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='book_lendings_student', to='app.student')),
            ],
            options={
                'verbose_name': 'Library Book Lending History',
                'verbose_name_plural': 'Library Book Lending Histories',
            },
        ),
    ]
