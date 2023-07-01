from .default import Default

class Development(Default):
    print("ENV: --- DEVELOPMENT ---")
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://EE2_DEV:12345678&ABCxyz@localhost:3306/estateelite2_dev'