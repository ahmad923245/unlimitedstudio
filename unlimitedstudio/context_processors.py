from unlimitedstudio import settings


def site_constants(request):
    # return the value you want as a dictionary. you may add multiple values in there.
    return {'APP_NAME': settings.APP_NAME, 'MEDIA_BASE_PATH': settings.MEDIA_URL}
