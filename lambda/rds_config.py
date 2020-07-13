#config file containing credentials for RDS MySQL instance
import os

db_username = os.environ['db_username']
db_password = os.environ['db_password']
db_name = os.environ['db_name']
db_endpoint = os.environ['db_endpoint']