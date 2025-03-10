from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from cart.cart import Cart
from courses.models import Course, Category
from udemy.models import Enroll

#integrating the proctoring part 
import requests # type: ignore
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def start_exam(request, course_id):
    """
    This function is triggered when a user completes a course.
    It sends a request to the proctor system to start an exam.
    """
    user_id = request.user.id
    course = get_object_or_404(Course, id=course_id)
    
    # Call the Flask API to start proctoring
    response = requests.post('http://localhost:5000/start_proctor', json={'user_id': user_id, 'course_id': course_id})

    if response.status_code == 200:
        #return redirect('http://localhost:5000/proctor_interface')  # Redirect user to the proctor system
        return render(request, 'exam.html')
    else:
        return render(request, 'error.html', {'message': 'Error starting proctoring session.'})
    





# proctoring part 




class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/details.html'
    context_object_name = 'course'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs.get(self.slug_url_kwarg)
        slug_field = self.get_slug_field()
        queryset = queryset.filter(**{slug_field: slug})
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': self.model._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object(self.get_queryset())
        if self.request.user.is_authenticated:
            if Enroll.objects.filter(course=course, user_id=self.request.user.id).exists():
                context['is_enrolled'] = True
            else:
                cart = Cart(self.request)
                context['is_in_cart'] = cart.has_course(course)
        else:
            cart = Cart(self.request)
            context['is_in_cart'] = cart.has_course(course)
        return context


class CoursesByCategoryListView(ListView):
    model = Course
    template_name = 'courses/courses_by_category.html'
    context_object_name = 'courses'

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        return self.model.objects.filter(category_id=category.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['slug'])
        context['category'] = category
        context['categories'] = Category.objects.all()
        return context
