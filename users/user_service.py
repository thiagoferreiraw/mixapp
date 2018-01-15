from users.models import User


class UserService:

    @staticmethod
    def check_user_permission(user_id, group_name):
        return User.objects.get(pk=user_id).groups.filter(name=group_name).exists()


