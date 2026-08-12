import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("COGNODB_URI")
username = os.getenv("COGNODB_USERNAME")
password = os.getenv("COGNODB_PASSWORD")

print("URI loaded:", bool(uri))
print("Username loaded:", username)
print("Password loaded:", bool(password))
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("COGNODB_URI")
username = os.getenv("COGNODB_USERNAME")
password = os.getenv("COGNODB_PASSWORD")

print("URI loaded:", bool(uri))
print("Username loaded:", username)
print("Password loaded:", bool(password))