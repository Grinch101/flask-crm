class Configuration:
    DEBUG = True


class DevelopmentConfig(Configuration):
    SECRET_KEY = "My_Key"
    TESTING = False

class ProductionConfig(Configuration):
    SECRET_KEY = 'aVeryHardToBreakKey'
    DEBUG = False

class TestingConfig(Configuration):
    TESTING = True
    USERNAME = 'admin'
    PASSWORD = 'admin'
    SECRET_KEY = "My_Key"
