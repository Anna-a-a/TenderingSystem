class Tender:
    def __init__(self, id, description, created_data_time, start_data_time, end_data_time, status_description,
                 user_name, user_login, supplier_id, supplier_name, supplier_price, is_winner):
        self.id = id
        self.description = description
        self.created_data_time = created_data_time
        self.start_data_time = start_data_time
        self.end_data_time = end_data_time
        self.status_description = status_description
        self.user_name = user_name
        self.user_login = user_login
        self.supplier_id = supplier_id
        self.supplier_name = supplier_name
        self.supplier_price = supplier_price
        self.is_winner = is_winner

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'created_data_time': self.created_data_time,
            'start_data_time': self.start_data_time,
            'end_data_time': self.end_data_time,
            'status_description': self.status_description,
            'user_name': self.user_name,
            'user_login': self.user_login,
            'supplier_id': self.supplier_id,
            'supplier_name': self.supplier_name,
            'supplier_price': self.supplier_price,
            'is_winner': self.is_winner
        }
