from EventsApp.models import User


def cron_job_delete_unverified():
    unwanted_users = User.objects.filter(is_active=False, profile_status=False)
    print(unwanted_users)
    unwanted_users.delete()