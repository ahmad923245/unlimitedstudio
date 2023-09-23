from setting.models import *
from django.http import HttpResponse

def StaticPageHtml(request, page_type):

    if request.method == 'GET':
        pp = StaticPages.objects.filter(page_type=page_type).last()
        content = ''
        if pp:
            content = pp.content
            if content:
                meta_content = '<html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head><body>' + content + '</body></html>'
                return HttpResponse(meta_content)
        else:
            return HttpResponse(content)