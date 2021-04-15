import os

class Configuration:
    DEBUG = True


class DevelopmentConfig(Configuration):
    SECRET_KEY = "My_Key"


class ProductionConfig(Configuration):
    SECRET_KEY = 'aVeryHardToBreakKey'
    DEBUG = False