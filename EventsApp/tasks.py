from background_task import background

from EventsApp.models import User


@background(schedule=60)
def delete_bots():
    unwanted_users = User.objects.filter(is_active=False, profile_status=False)
    print(unwanted_users)
    unwanted_users.delete()
