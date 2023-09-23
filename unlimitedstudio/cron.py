from .settings import base_url

def my_scheduled_job():
    print("sheduled_job")
    print('base :', base_url)
    url = str(base_url) + '/api/v1/booking/cron/'
    try:
        import requests
        x = requests.get(url)
        print("get_url")
        print('api calling : ', requests.Response(x))
    except Exception as e:
        print(str(e))
    pass

