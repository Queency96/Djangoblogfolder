from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, student_position, Cohort_Group, Program, Student_Profile
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib import messages
from django.core.exceptions import ValidationError
from datetime import datetime, date
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# E-mail validator
def mail_validator(value):
    if '@' in value and '.com' in value:
        return value
    else:
        raise ValidationError('Invalid email address')

# List of student 
@login_required(login_url='/login')
def student_list(request):   
    student_list = Student.objects.all()
    paginator = Paginator(student_list, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    # extracting student's type from data base and pass it to template as options
    student_type = student_position
    
    # extracting cohorts' name from data base and pass it to template as options
    all_cohorts = Cohort_Group.objects.all()
    
    # Pass the student data to the template
    context = {
        'students': page_obj,
        'type': student_type,
        'all_cohorts': all_cohorts,
    }
    return render(request, 'blog/studentlist.html', context)

# Displaying student's profile dynamically
def get_profile_from_student(request, slug):   
    student = get_object_or_404(Student, slug=slug)  
    context = {
        'student': student
    }
    return render(request, 'blog/studentprofile.html', context)

# Sending Email messages to student
def message(request):
    if request.method == 'POST':
        # receiver's E-mail data
        email = request.POST.get('receiver_email')
        
        # Messages
        subject = request.POST.get('subject')
        pre_message = request.POST.get('message')
        
        # sender's data
        sender_name = request.POST.get('sender_name')
        sender_phone = request.POST.get('sender_phone')
        sender_email = request.POST.get('sender_email')
        
        message = f"""        
        Subject: {subject}
        
        {pre_message}
        
        From: {sender_name},                Phone: {sender_phone}
        E-mail: {sender_email}
        """
        # setting up variable for previous url
        previous_url = request.META.get('HTTP_REFERER', 'student_profile')  # Default to 'student_profile' if no referer
        
        # Check if all fields are filled
        if email and sender_name and sender_phone and sender_email and pre_message:
            try:
                validated_email = mail_validator(email)  # Validate email
                send_student_email(request, sender_email, message, subject, [validated_email])
                messages.success(request, 'Message sent successfully')
                return redirect(previous_url)
            except ValidationError as e:
                messages.error(request, 'Message not sent', text=str(e))
                return redirect(previous_url)
        else:
            messages.error(request, 'Do you fill all fields?')
            return redirect(previous_url)

# Function to delete student from database
def del_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    previous_url = request.META.get('HTTP_REFERER', 'student_list') 
    
    student.delete()
    return redirect(previous_url)

# Function to create new student to database
def create_student(request):
    if request.method == 'POST':
        students = Student.objects.all()
            
        previous_url = request.META.get('HTTP_REFERER', 'student_list') 
        
        # Student model inputs
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_type = request.POST.get('role')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        # Student profile inputs
        bio = request.POST.get('bio')
        DOB = request.POST.get('DOB')
        address = request.POST.get('address')
        rating = request.POST.get('rating') or 0.0  # Default rating if not provided
        profile_picture = request.FILES.get('profileImage')
        
        # Student course input
        course = request.POST.get('program')
        
        # Student cohort group input
        cohort = request.POST.get('cohort')

        # Validation for empty fields
        required_fields = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'bio': bio,
            'Date_of_birth': DOB,
            'address': address,
            'rating': rating,
            'profile_picture': profile_picture,
            'course': course,
            'cohort': cohort
        }
        
        for field, value in required_fields.items():
            if not value:
                messages.warning(request, f'{field.replace("_", " ").capitalize()} cannot be empty')
                return redirect(previous_url)
                
        student_roles = []
        for student in students:
            student_roles.append(student.student_type)
            
        # Check for role conflicts (President, Vice President)
        if 'President' in student_roles and student_type == 'President':
            messages.warning(request, 'President role already taken')
            return redirect(previous_url)
        elif 'Vice President' in student_roles and student_type == 'Vice President':
            messages.warning(request, 'Vice President role already taken')
            return redirect(previous_url)

        try:
            # Create new student and related records
            new_student = Student.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
                student_type=student_type,
                email=email,
                phone=phone
            )
            
            Student_Profile.objects.create(
                student=new_student,
                bio=bio,
                DOB=DOB,
                address=address,
                rating=rating,
                profile_picture=profile_picture,
            )
            
            Program.objects.create(
                student=new_student,
                courses=course,
            )
            
            Cohort_name = Cohort_Group.objects.get(name = cohort)
            Cohort_name.students.add(new_student)

            
            messages.success(request, 'User created successfully')
            return redirect(previous_url)
        except Exception as e:
            messages.error(request, f'Error: {e}')
            return redirect(previous_url)

# Function to create new cohort to database
def create_cohort(request):
    cohort_name = request.POST.get('addcohort')
    previous_url = request.META.get('HTTP_REFERER', 'student_list') 
    try:
        Cohort_Group.objects.create(name = cohort_name)
        messages.success(request, 'Cohort created successfully')
        return redirect(previous_url)
    except Exception as e:
        messages.error(f'Error occur: {e}')
        return redirect(previous_url)

def edit_views(request, slug):
    student = get_object_or_404(Student, slug=slug)
    all_cohorts = Cohort_Group.objects.all()
    student_type = student_position
    context ={
        'student': student,
        'all_cohorts': all_cohorts,
        'type': student_type
    }
    return render(request, 'blog/editstudent.html', context)

# Function to edit students details in database
def edit_student(request, slug):
    if request.method == 'POST':
        student = get_object_or_404(Student, slug=slug)

        # Update only fields that are provided
        updated = False
        student.username = request.POST.get('username', student.username)
        student.first_name = request.POST.get('first_name', student.first_name)
        student.last_name = request.POST.get('last_name', student.last_name)
        student.student_type = request.POST.get('role', student.student_type)
        student.email = request.POST.get('email', student.email)
        student.phone = request.POST.get('phone', student.phone)
        try:
            
            # Save changes to the `Student` model
            if student._state.db != '':  # Check if any field has been set differently
                student.save()
                updated = True
                messages.success(request, 'Student details updated successfully!')

            # Update the related `Student_Profile` model
            try:
                student_profile = Student_Profile.objects.get(student=student)
                profile_updated = False

                bio = request.POST.get('bio')
                DOB = request.POST.get('DOB')
                address = request.POST.get('address')
                rating = request.POST.get('rating')
                profile_picture = request.FILES.get('profileImage')

                if bio and student_profile.bio != bio:
                    student_profile.bio = bio
                    profile_updated = True
                if DOB and student_profile.DOB != DOB:
                    student_profile.DOB = DOB
                    profile_updated = True
                if address and student_profile.address != address:
                    student_profile.address = address
                    profile_updated = True
                if rating and student_profile.rating != float(rating):
                    student_profile.rating = float(rating)
                    profile_updated = True
                if profile_picture:
                    student_profile.profile_picture = profile_picture
                    profile_updated = True

                if profile_updated:
                    student_profile.save()
                    messages.success(request, 'Student profile updated successfully!')
            except Student_Profile.DoesNotExist:
                messages.warning(request, 'Student profile not found. Please create it first.')

            # Update the `Program` model
            course = request.POST.get('program')
            if course:
                try:
                    program = Program.objects.get(student=student)
                    if program.courses != course:
                        program.courses = course
                        program.save()
                        messages.success(request, 'Program updated successfully!')
                except Program.DoesNotExist:
                    messages.warning(request, 'Program data not found.')

            # Update the `Cohort_Group` model
            cohort = request.POST.get('cohort')
            if cohort:
                try:
                    # Get the new cohort group by name
                    cohort_group = Cohort_Group.objects.get(name=cohort)
                    
                    
                    # Check if the student is already part of any other cohort groups
                    old_cohorts = Cohort_Group.objects.filter(students=student)
                    if old_cohorts.exists():
                        # Remove the student from all old cohort groups to stop student having more than one cohorts group
                        for old_cohort in old_cohorts:
                            old_cohort.students.remove(student)

                    # Add the student to the new cohort group
                    if student not in cohort_group.students.all():
                        cohort_group.students.add(student)
                        messages.success(request, f'{student.username} {student.last_name} updated successfully!')
                    else:
                        messages.warning(request, f'{student.first_name} {student.last_name} is already in the cohort group {cohort_group.name}.')
                
                except Cohort_Group.DoesNotExist:
                    messages.warning(request, 'Cohort group not found.')
            messages.success(request, f'{student.first_name} {student.last_name} updated successfully!')
            # Redirect back to the referring page or a default page
            return redirect('student_list')
        except Exception as e:
            messages.warning(request, f' Error: {e}, {student.first_name} {student.last_name} does not updated')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('student_list')

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/student_list')
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {'form': form})

# Email message instance logic
def send_student_email(request, sender_email, message, subject, recipient_list):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=sender_email, 
            recipient_list=recipient_list, 
            fail_silently=False,
        )
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")  # Pass request to messages.error