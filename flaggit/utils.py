from django.contrib.contenttypes.models import ContentType
from flaggit.models import Flag, FlagInstance

def flag(obj, user=None, ip=None, comment=None):
    flag, created = Flag.objects.get_or_create(
        object_id=obj.pk,
        content_type=ContentType.objects.get_for_model(obj)
    )
    
    if user:
        flag_instance, created = FlagInstance.objects.get_or_create(
            flag=flag,
            user=user,
        )
    else:
        flag_instance, created = FlagInstance.objects.get_or_create(
            flag=flag,
            ip=ip
        )
    flag_instance.ip = ip
    flag_instance.comment = comment

    #
    # In future flag_type will be based upon the comment
    # flag is by default 1 which is Inappropriate
    # move to other places can be handled with keyword in comments
    # as comments will be fixed options for user
    #
    # flag_instance.flag_type = flag_type

    flag_instance.save()
    
    return flag_instance
    
