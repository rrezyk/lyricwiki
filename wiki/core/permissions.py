from wiki.conf import settings

# Object settings.
def can_assign(object, user):
    return not user.is_anonymous() and settings.CAN_ASSIGN(object, user)
def can_assign_owner(object, user):
    return not user.is_anonymous() and settings.CAN_ASSIGN_OWNER(object, user)
def can_change_permissions(object, user):
    return not user.is_anonymous() and settings.CAN_CHANGE_PERMISSIONS(object, user)
def can_delete(object, user):
    return not user.is_anonymous() and settings.CAN_DELETE(object, user)
def can_moderate(object, user):
    return not user.is_anonymous() and settings.CAN_MODERATE(object, user)
def can_admin(object, user):
    return not user.is_anonymous() and settings.CAN_ADMIN(object, user)
