from django.urls import include, path
from .views import *

app_name = 'courses'


urlpatterns = [
    path('courses/<slug:slug>', CourseDetailView.as_view(), name='course-details'),
    path('courses/<slug:slug>/category', CoursesByCategoryListView.as_view(), name='course-by-category'),
    # proctoring integrating part 
    path('start-exam/<int:course_id>/', start_exam, name='start_exam'),
    #proctroing integrating part 

    #payment template
    #path('payments/', include('payments.urls')),



]
