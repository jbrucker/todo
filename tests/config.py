"""Root path of the API for tests to use when constructing URLs."""
from decouple import config

# Use an empty string for no prefix: ROOT_PATH = ""

ROOT_PATH = config("ROOT_PATH", default="/api")
