from django.contrib import admin

from .models import UserProfile, Task

# Register your models here.
class TaskInLine(admin.TabularInline):
	model = Task
	extra = 2


class UserAdmin(admin.ModelAdmin):
	list_display = ('user', 'backgroundimage', 'creationdate')
	list_filter = ['creationdate']

	search_fields = ['user']


	fieldsets = [ ('Account',	#First Element is the title of the FieldSet
						{'fields' : ['user'] }),
	 			  ('Account Information',
	 			  		{'fields' : ['creationdate', 'backgroundimage'] }),
	 			]
	inlines = [TaskInLine]

admin.site.register(UserProfile, UserAdmin)
#admin.site.register(Task)