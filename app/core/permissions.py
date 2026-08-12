class Permission:
    # Product
    PRODUCT_READ = "product:read"
    PRODUCT_CREATE = "product:create"
    PRODUCT_UPDATE = "product:update"
    PRODUCT_DELETE = "product:delete"

    # Task
    TASK_VIEW = "task:view"
    TASK_CREATE = "task:create"
    TASK_UPDATE = "task:update"
    TASK_DELETE = "task:delete"


ROLE_PERMISSIONS = {
    "admin": [
        # Product
        Permission.PRODUCT_READ,
        Permission.PRODUCT_CREATE,
        Permission.PRODUCT_UPDATE,
        Permission.PRODUCT_DELETE,
        # Task
        Permission.TASK_VIEW,
        Permission.TASK_CREATE,
        Permission.TASK_UPDATE,
        Permission.TASK_DELETE,
    ],
    "manager": [
        # Task only
        Permission.TASK_VIEW,
        Permission.TASK_CREATE,
        Permission.TASK_UPDATE,
    ],
    "editor": [
        # Product only
        Permission.PRODUCT_READ,
        Permission.PRODUCT_CREATE,
        Permission.PRODUCT_UPDATE,
    ],
    "user": [
        # Product only
        Permission.PRODUCT_READ,
    ],
}
