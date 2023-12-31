""" Constants for the mahdil app """

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# SITE_ID = 1

SECRET_KEY = '=fq!b1)k&smnvc8zw!ik7v$r+340g#4(rh^i-9)+qqe@j8)r4z'

# MAHDIL CONSTANTS
MAHDIL_LIVE = False
MAHDIL_BD_TEAM = True
MAHDIL_SQLITE = False
MAHDIL_SQL = 'web_capsulier'
PASSWORD_SQL_MAHDIL_LIVE = ''
MAHDIL_HOST = 'localhost'
MAHDIL_STATIC_LOCAL = True
MAHDIL_MEDIA_LOCAL = True
LIVE_TEST = False
PAYMENT_PRODUCTION = False

# GOOGLE MAPS
if MAHDIL_LIVE:
    GEOPOSITION_GOOGLE_MAPS_API_KEY = ''
else:
    GEOPOSITION_GOOGLE_MAPS_API_KEY = 'AIzaSyDdfNK2L9RMM7YFCo8g9YaZHcm-qqPscfI'

# MAILCHIMP
if MAHDIL_LIVE:
    MAILCHIMP_API_KEY = ''
    MAILCHIMP_LIST_ID = ''
else:
    MAILCHIMP_API_KEY = '8e1fa74476cf67adce093ac2c34ed9b8-us14'
    MAILCHIMP_LIST_ID = '452d50c560'

# ADMIN MAIL
ADMIN = ''

# FOR MORE THEN ONE ADMIN MAIL
# ADMIN = 'ak@mahdil.com', 'sathi@mahdil.com'

# RECATCHA
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''

NOCAPTCHA = True
