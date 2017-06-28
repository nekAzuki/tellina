from django.contrib import admin

from .models import Annotation, Command, CommandAdmin, NLRequest, Translation, URL, URLTag, User

admin.site.register(Command, CommandAdmin)
admin.site.register(URL)
admin.site.register(User)
admin.site.register(NLRequest)
admin.site.register(Translation)
admin.site.register(Annotation)
admin.site.register(URLTag)
