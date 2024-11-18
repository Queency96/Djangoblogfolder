from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib import messages
from django.core.exceptions import ValidationError


def mail_validator(value):
    if '@' in value and '.com' in value:
        return value
    else:
        raise ValidationError('Invalid email address')

def student_list(request):   
    student_list = Student.objects.all()
    paginator = Paginator(student_list, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # Pass the student data to the template
    context = {
        'students': page_obj
    }
    return render(request, 'blog/studentlist.html', context)

def get_profile_from_student(request, slug):   
    student = get_object_or_404(Student, slug=slug)  
    context = {
        'student': student
    }
    return render(request, 'blog/studentprofile.html', context)

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

def del_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    previous_url = request.META.get('HTTP_REFERER', 'student_list') 
    
    student.delete()
    return redirect(previous_url)

def create_student(request):
    if request.method == 'POST':
        # Student model inputs
        username = request.POST.get('username'),
        first_name = request.POST.get('first_name'),
        last_name = request.POST.get(),
        student_type = request.POST.get(),
        status = request.POST.get(),
        email = request.POST.get(),
        phone = request.POST.get(),
        
        # Student profile inputs
        bio = request.POST.get(),
        DOB = request.POST.get(),
        address = request.POST.get(),
        rating = request.POST.get(),
        profile_picture = request.FILE.get('profileImage'),
        date_join = request.POST.get(),
        
        # Student course input
        course = request.POST.get(),
        
        # Student cohort group input
        cohort = request.POST.get(),
        date_join = request.POST.get(),


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