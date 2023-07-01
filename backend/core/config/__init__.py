from os import getenv
from dotenv import load_dotenv

load_dotenv()

ENV = getenv('ENV')

def load_config(env=ENV):
    if env == 'production':
        from .production import Production
        return Production()
    elif env == 'testing':
        from .testing import Testing
        return Testing()
    else:
        from .development import Development
        return Development()