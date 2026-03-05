# views.py
import csv
from django.shortcuts import render, redirect
from .models import Student
from .forms import CSVUploadForm
from django.core.mail import send_mail
from django.conf import settings

def indexpage(request):
    return render(request, "index.html",)

def upload(request):
    return render(request, "upload.html",)



def display_data(request):
    # Fetch all student records from the database
    students = Student.objects.all()
    # Pass the student data to the template
    return render(request, 'display_data.html', {'students': students})

def upload_attendance(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                student = Student(
                    name=row['name'],
                    course=row['course'],
                    time_spent=row['timeSpent'],
                    late_entries=row['lateEntries'],
                    early_exits=row['earlyExits'],
                    attendance_status=row['attendanceStatus'],
                    threshold_alert=row['thresholdAlert'] == 'True',
                    email=row['email']
                )
                student.save()

            return redirect('success')  # Redirect to a success page
    else:
        form = CSVUploadForm()
    return render(request, 'upload.html', {'form': form})

def success(request):
    return render(request, 'success.html')

def email(request):
    return render(request,'email.html')
# views.py
def send_emails(request):
    students = Student.objects.all()
    for student in students:
        subject = f"Attendance Summary for {student.course}"
        message = f"Dear {student.name},\n\nHere is your attendance summary:\n\nTime Spent: {student.time_spent}\nLate Entries: {student.late_entries}\nEarly Exits: {student.early_exits}\nAttendance Status: {student.attendance_status}"

        if student.threshold_alert:
            message += "\n\n⚠️ Your attendance is below the required threshold. Please improve your attendance to avoid issues."
        else:
            message += "\n\nYour attendance is in good standing. Keep it up!"

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [student.email],
            fail_silently=False,
        )

    return redirect('success')


def attendance_reports(request):
    # Fetch all student records from the database
    attendance_records = Student.objects.all()

    # Prepare data for the charts
    labels = [record.name for record in attendance_records]
    attendance_data = [1 if record.attendance_status == 'Present' else 0 for record in attendance_records]

    # Assuming time_spent is stored in hours as a string like '10h 30m'
    time_spent_data = []
    for record in attendance_records:
        hours = record.time_spent.split('h')[0]  # Extract only the hour part (assuming the format is consistent)
        time_spent_data.append(float(hours))

    late_entries_data = [record.late_entries for record in attendance_records]

    context = {
        'attendance_records': attendance_records,
        'labels': labels,
        'attendance_data': attendance_data,
        'time_spent_data': time_spent_data,
        'late_entries_data': late_entries_data,
    }

    # Render the report page with context data for the charts and table
    return render(request, 'report.html', context)
