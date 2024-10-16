from django.shortcuts import render, get_object_or_404
from .models import Student, Student_Profile, Cohort_Group, Program

def student_list(request):
    # Get all students
    students = Student.objects.all()

    # Prepare a list to store the student data
    student_data = []

    for student in students:
        student_id = student.id
        # Get the student's program
        try:
            program = Program.objects.get(student=student)
        except Program.DoesNotExist:
            program = None  # Handle if no program exists for the student

        # Get the student's profile
        try:
            profile = Student_Profile.objects.get(student=student)
        except Student_Profile.DoesNotExist:
            profile = None  # Handle if no profile exists for the student

        # Get the cohort groups the student belongs to
        cohort_groups = Cohort_Group.objects.filter(students=student)
        cohort_group_names = ', '.join([cohort.name for cohort in cohort_groups])

        # Prepare the data for each student
        student_data.append({
            'first_name': student.first_name,
            'last_name': student.last_name,
            'program': program.courses if program else 'N/A',  # Show the program's course or N/A
            'date_joined': profile.date_join if profile else 'N/A',  # Handle if profile is None
            'status': student.status,
            'cohort_group': cohort_group_names,
            'rating': profile.rating if profile else 'N/A',  # Handle if profile is None
            'profile_id': student_id,  # Keep track of the student id for linking
            'profile_picture': profile.profile_picture.url if profile and profile.profile_picture else 'N/A',  # Handle profile picture if None
        })

    # Pass the student data to the template
    context = {
        'students': student_data
    }
    return render(request, 'blog/studentlist.html', context)


def get_profile_from_student(request, student_id):
    # Get the student by id
    student = get_object_or_404(Student, id=student_id)
    
    # Access the related Student_Profile
    try:
        profile = student.student_profile  # Assumes Student_Profile has a OneToOneField with Student
    except Student_Profile.DoesNotExist:
        profile = None

    # Get cohort groups the student is part of
    cohort_groups = Cohort_Group.objects.filter(students=student)
    cohort = ', '.join([cohort.name for cohort in cohort_groups]) if cohort_groups.exists() else 'No Cohort'

    # Get all students in this student's cohorts, excluding the current student
    members = Student.objects.filter(cohort_group__in=cohort_groups).exclude(id=student.id).distinct()  # Exclude the current student

    # Create a list to hold member data
    cohort_data = []
    
    for member in members:
        # Get the member's profile and program details
        try:
            member_profile = member.student_profile
        except Student_Profile.DoesNotExist:
            member_profile = None

        member_program = Program.objects.filter(student=member).first()  # Assuming one program per student
        
        # Add relevant information to the list
        cohort_data.append({
            'name': f"{member.first_name} {member.last_name}",
            'profile_picture': member_profile.profile_picture.url if member_profile and member_profile.profile_picture else None,
            'program': member_program.courses if member_program else 'No Program',
        })

    context = {
        'username': student.username,
        'student': student,
        'status': student.status,
        'cohort': cohort,
        'profile_id': profile.id if profile else None,
        'bio': profile.bio if profile else 'No Bio',
        'DOB': profile.DOB if profile else 'N/A',
        'address': profile.address if profile else 'N/A',
        'rating': profile.rating if profile else 'N/A',
        'DP': profile.profile_picture.url if profile and profile.profile_picture else 'N/A',
        'D_joined': profile.date_join if profile else 'N/A',
        'cohort_members': cohort_data,  # This will now exclude the current student
    }

    return render(request, 'blog/studentprofile.html', context)
