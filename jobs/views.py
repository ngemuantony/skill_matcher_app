from django.utils.timezone import now
from django.core.mail import send_mail
from django.shortcuts import render
from .models import Job, JobAlert
import requests

def fetch_jobs_view(request):
    if request.method == 'POST':
        skills = request.POST.get('skills').split(',')
        # Assuming we have an API endpoint to fetch jobs by skills
        url = 'https://tabiya.api/jobs?skills=' + ','.join(skills)
        
        try:
            # Make the API call to fetch jobs
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            jobs = response.json()

            # Save jobs to the database
            for job_data in jobs:
                Job.objects.get_or_create(
                    title=job_data['title'],
                    defaults={
                        'description': job_data['description'],
                        'location': job_data['location'],
                        'company': job_data['company'],
                        'skills_required': job_data['skills'],
                        'posted_date': now()  # Ensure you have this field in your model
                    }
                )

            # Render the job list template with the fetched jobs
            return render(request, 'jobs/job_list.html', {'jobs': jobs})

        except requests.RequestException as e:
            # Handle errors from the API request
            return render(request, 'jobs/job_search.html', {'error': str(e)})

    # Render the job search template for GET requests
    return render(request, 'jobs/job_search.html')


def check_new_jobs():
    alerts = JobAlert.objects.all()
    for alert in alerts:
        skills = alert.skills.split(',')
        jobs = Job.objects.filter(skills_required__icontains=skills, posted_date__gt=alert.last_checked)
        if jobs.exists():
            # Send notification email
            send_mail(
                'New Job Alerts',
                f"Hi {alert.user.username}, new jobs matching your skills are available!",
                'from@example.com',
                [alert.user.email],
                fail_silently=False,
            )
            # Update the last checked time
            alert.last_checked = now()
            alert.save()


def job_list(request):
    # Fetch jobs from your database
    jobs = Job.objects.all()  # Fetch all jobs from the database
    context = {'jobs': jobs}
    return render(request, 'jobs/job_list.html', context)  # Render job list template


def job_search(request):
    # This function seems redundant since fetch_jobs_view does the job searching.
    return render(request, 'jobs/job_search.html')  # Render job search template
