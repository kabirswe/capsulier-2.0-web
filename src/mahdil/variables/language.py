from mahdil.variables.env_variables import *

gettext = lambda s: s

LANGUAGES = (
    ('fr', gettext('French')),
    ('en', gettext('English')),
    ('es', gettext('Spanish')),
)

MODELTRANSLATION_FALLBACK_LANGUAGES = ('fr', 'en', 'es')


if MAHDIL_BD_TEAM:
    LANGUAGE_CODE = 'en-GB'
else:
    LANGUAGE_CODE = 'fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True
