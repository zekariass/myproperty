from .base import *

IS_DEVELOPMENT_ENV = getenv("IS_DEVELOPMENT")

IS_DEVELOPMENT = True if str(IS_DEVELOPMENT_ENV).lower() == "true" else False

if IS_DEVELOPMENT:
    print("STARTING DEV SERVER.....")
    from .development import *
else:
    print("STARTING PROD SERVER.....")
    from .production import *
