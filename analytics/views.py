from datetime import timedelta

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models.functions import TruncMonth
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, F
from django.http.response import JsonResponse
from django.utils import timezone

from note.models import Note


def jsonify_queryset(object,fields):
    return simplejson.dumps(list(object.values(*fields.split(','))))


# Create your views here.
def analytics_home(request):
    template_name = 'analytics.html'
    context = {}
    user = request.user
    if not user.is_authenticated:
        messages.add_message(
            request,
            messages.ERROR,
            'You need to log in first!'
        )
        return redirect('login_view')
    return render(request, template_name, context)


def get_analytics_data(request):
    user = request.user
    current_date = timezone.now().date()
    user_register_date = user.date_joined.date()

    completed_notes_counts = []
    date = user_register_date
    date_interval_dates = []
    while date <= current_date:
        next_month = (date + timedelta(days=31)).replace(day=1)
        notes_completed_count = Note.objects.filter(
            author=user,
            completed_at__date__gte=date,
            completed_at__date__lt=next_month
        ).count()
        month_name = date.strftime('%B')
        completed_notes_counts.append(notes_completed_count)
        date_interval_dates.append((month_name, date.year))
        date = next_month

    max_completed = max(completed_notes_counts)
    prepared_chart_data = {
        'labels': date_interval_dates,
        'values': completed_notes_counts,
        'maxValueY': max_completed + 3
    }
    chart_data = prepared_chart_data
    return JsonResponse(data=chart_data, safe=False)
