# TenderingSystem
tendering system for university project

1.function names function_name() 
2.commits only in english
3.make new code ONLY in your own branch
4. def add_certificate(self, dict_of_value: dict) -> bool:
        """
        :param dict_of_value данные сертификата
        :return: None
        добавляет сертификат в бд
        """
        list_of_value = list(dict_of_value.values())


# Set up environment
1. установить docker
2. установить docker-compose
3. pyway migrate
4. docker pull postgres
 

#  Run db locally:
1. run container with db :
   docker-compose up --force-recreate --remove-orphans --build
2. pyway migrate

# Clean db 
docker-compose down -v

# Connect to db
user: username
password: password
port: 5432
default database: tendering-system-db

Test data and scheme - db/init.sql

#-- Insert a PDF file into the database as binary data
INSERT INTO documents (file_name, file_data)
VALUES ('example.pdf', pg_read_binary_file('/path/to/example.pdf'));


