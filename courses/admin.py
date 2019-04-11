from django.contrib import admin

# Register your models here.
from .forms import LectureAdminForm
from .models import Course, Lecture, MyCourses, Topic, Review, Certificate, MyLecture


class MyLectureAdmin(admin.ModelAdmin):
    list_display = ['lecture', 'topic','user',]
    search_fields = ['lecture','user',]
    readonly_fields = ['updated', 'timestamp', 'lecture','user', 'topic']

    class Meta:
        model = MyLecture


class CertificateAdmin(admin.ModelAdmin):
    list_display = ['course','user',]
    search_fields = ['course','user',]

    class Meta:
        model = Certificate


class MyCoursesAdmin(admin.ModelAdmin):
    list_display = ['user', 'short_title',]
    search_fields = ['user', 'short_title']

    class Meta:
        model = MyCourses

    def short_title(self, obj):
        return str(obj.courses.all().count())


class TopicInline(admin.TabularInline):
    model = Topic    
    extra = 1

class LectureInline(admin.TabularInline):
    model = Lecture
    form = LectureAdminForm
    prepopulated_fields = {"slug": ("title",)}
    extra = 1

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    inlines = [TopicInline, LectureInline, ReviewInline]
    list_filter = ['updated', 'timestamp']
    list_display = ['title', 'updated', 'timestamp', 'order']
    readonly_fields = ['updated', 'timestamp', 'short_title']
    search_fields = ['title', 'description']
    list_editable = ['order']

    class Meta:
        model = Course

    def short_title(self, obj):
        return obj.title[:3]

admin.site.register(Course, CourseAdmin)
admin.site.register(MyCourses, MyCoursesAdmin)
admin.site.register(Certificate, CertificateAdmin)
admin.site.register(MyLecture, MyLectureAdmin)
