from .default import Default

class Testing(Default):
    print("ENV: --- TESTING ---")
    DEBUG = True
    TESTING = True
    PORT = 5001
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://EE2_TEST:12345678&ABCxyz@localhost:3306/estateelite2_test'