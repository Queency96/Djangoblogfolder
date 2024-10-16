from django.shortcuts import render




def About_us(request):
    return render(request, "blog/about.html")




def Contact_us(request):
    return render(request, "blog/contact.html")








