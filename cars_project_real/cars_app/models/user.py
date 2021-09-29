class User:
    # CLASS ATTRIBUTE
    def __init__(self, data):
        # ATTRIBUTES
        self.id = data['id']
        self.frist_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']