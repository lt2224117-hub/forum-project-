from django.shortcuts import render
from forum.models import Topic

def search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Topic.objects.filter(
            title__icontains=query
        ).select_related('author', 'category').order_by('-created_at')
    return render(request, 'search/search.html', {
        'query': query,
        'results': results,
    })