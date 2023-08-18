from easy_thumbnails.conf import Settings as thumbnail_settings

# Cropping
THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS
THUMBNAIL_SUBDIR = 'thumbs'
# IMAGE_CROPPING_JQUERY_URL = 'adminsortable2/js/plugins/admincompat.js'
