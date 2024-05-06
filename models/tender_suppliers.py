class Tender_suppliers:
    def __init__(self, id, description, created_date_time, start_date_time, end_date_time, first_price, title,
                 delivery_address, delivery_area, status_description, user_name, user_login, supplier_ids, supplier_names,
                 supplier_logins, supplier_prices, supplier_price, is_winner):
        self.id = id
        self.description = description
        self.created_date_time = created_date_time
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.first_price = first_price
        self.title = title
        self.delivery_address = delivery_address
        self.delivery_area = delivery_area
        self.status_description = status_description
        self.user_name = user_name
        self.user_login = user_login
        self.supplier_ids = supplier_ids
        self.supplier_names = supplier_names
        self.supplier_logins = supplier_logins
        self.supplier_prices = supplier_prices
        self.supplier_price = supplier_price
        self.is_winner = is_winner

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'created_date_time': self.created_date_time,
            'start_date_time': self.start_date_time,
            'end_date_time': self.end_date_time,
            'first_price': self.first_price,
            'title': self.title,
            'delivery_address': self.delivery_address,
            'delivery_area': self.delivery_area,
            'status_description': self.status_description,
            'user_name': self.user_name,
            'user_login': self.user_login,
            'supplier_ids': self.supplier_ids,
            'supplier_names': self.supplier_names,
            'supplier_logins': self.supplier_logins,
            'supplier_prices': self.supplier_prices,
            'supplier_price': self.supplier_price,
            'is_winner': self.is_winner
        }
