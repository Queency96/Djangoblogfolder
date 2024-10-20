from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages


# Create your views here.

def Bloghome(request):   
    return render(request, "blog/index.html")

def Post_list(request):
    return render(request, "blog/post.html")

def about_us(request):
    return render(request, "blog/about.html")


def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        message1 = request.POST.get('message')
        message = f"From: {name} Email: {email}" " \n" + " \n" + message1 + "\n" + "\n" + f"Call on:{phone_number}"
        
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