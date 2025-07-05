class Config():
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    DEBUG = True
    SECRET_KEY = 'shhhh... its very secret'
    
    # SECURITY_LOGIN_URL = '/W567890OIJHB'
    SECURITY_TRACKABLE = True
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'