from faker import Faker

fake = Faker()

BASE_URL = "https://www.automationteststore.com"
BASE_URL_NO_WWW = "https://automationteststore.com"

U_NAME = fake.user_name().replace(" ", "_").lower()
#U_PASS = fake.password("")
# E_MAIL = fake.email()
# U_NAME = "mama_p_papa"
# U_PASS = "mama_papa"
# E_MAIL = "mama@papa.ru"
E_MAIL = f"{U_NAME}@gmail.com"
U_PASS = "Aa1!StrongPass99"

DATA_REGISTER_LOGIN = {
    "csrftoken": "None",
    "csrfinstance": "0",
    "firstname": "mamasita",
    "lastname": "papasita",
    "email": E_MAIL,
    "telephone": "987-654-3210",
    "loginname": U_NAME,
    "password": U_PASS,
    "confirm": U_PASS,
    "agree": "1",
    # "account": "register"
    }

DATA_REGISTER_LOGIN_FULL = {
    "csrftoken": "None",
    "csrfinstance": "0",
    "firstname": "mama",
    "lastname": "papa",
    "email": E_MAIL,
    "telephone": "123-456-7890",
    "company": "AQA Course",
    "address_1": "Address",
    "address_2": "",
    "city": "Ulyanovsk",
    # "postcode": "432054",
    # "country_id": "176",
    # "zone_id": "2795",
    # "country_id": "223",   # United States
    # "zone_id": "3655",     # California
    "postcode": "12345",
    "country_id": "223",  # USA
    "zone_id": "3655",  # California
    "loginname": U_NAME,
    "password": U_PASS,
    "confirm": U_PASS,
    "newsletter": "0",
    "agree": "1",
#    "account": "register"
    }

# DATA_REGISTER = {
#     "csrftoken": "None",
#     "csrfinstance": "3",
#     "account": "register"
#     }

DATA_LOGIN = {
    "csrftoken": "None",
    "csrfinstance": "0",
    "loginname": U_NAME,
    "password": U_PASS,
    "account": "login"
    }
