from django.shortcuts import render, redirect
from .models import Student, Student_Profile, Cohort_Group, Program
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib import messages

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



def get_profile_from_student(request, student_id):   
    student = Student.objects.get(id=student_id)  
    context = {
        'student' : student
    }
    return render(request, 'blog/studentprofile.html', context)

def message(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        message1 = request.POST.get('message')
        
        
        # Check if all fields are filled
        if name and email and phone_number and message1:
            # Send email to the superuser admin
            send_welcome_email(request, name, email, message)
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact_us')  # Redirect after submission
        else:
            messages.error(request, 'Please fill in all fields.')

    return render(request, 'blog/contact.html')


def send_welcome_email(request, name, email, message):
    try:
        send_mail(
            subject=f"New contact message from {name}",
            message=message,
            from_email= email,  # Email of the customer
            recipient_list=['queency96@gmail.com', 'hilsoniyke@gmail.com', 'lenzboivick@gmail.com'],  # Corrected to a list
            fail_silently=False,
        )
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")  # Pass request to messages.error
