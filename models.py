
class User:


    def __init__(self, full_name, username, role, campus_id=None):
        self.full_name = full_name
        self.username = username
        self.role = role
        self.campus_id = campus_id


class Lecturer(User):


    def __init__(self, full_name, username, campus_id=None):
        super().__init__(full_name, username, "Lecturer", campus_id)


class CampusAdministrator(User):


    def __init__(self, full_name, username, campus_id):
        super().__init__(
            full_name,
            username,
            "Campus Administrator",
            campus_id
        )


class SystemOperator(User):


    def __init__(self, full_name, username):
        super().__init__(full_name, username, "System Operator")


class Resource:


    def __init__(self, resource_code, name, resource_type, campus_id):
        self.resource_code = resource_code
        self.name = name
        self.resource_type = resource_type
        self.campus_id = campus_id
        self.active = True

    def deactivate(self):

        self.active = False

    def activate(self):

        self.active = True
