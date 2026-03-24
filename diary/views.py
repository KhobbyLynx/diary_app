from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from .models import DiaryEntry
import json
import logging

logger = logging.getLogger(__name__)


def get_ai_insights(content):
    # Fetch summary and emotion from Groq API with fallback
    try:
        from groq import Groq

        api_key = settings.GROQ_API_KEY
        if not api_key:
            return {
                'summary': 'Unable to analyze — API key not configured.',
                'emotion': 'Neutral',
            }

        client = Groq(api_key=api_key)

        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a sensitive diary assistant. Analyze the text "
                        "and return a JSON object with two keys: "
                        "'summary' (a 15-word max summary for social sharing) "
                        "and 'emotion' (a single-word emotional state like "
                        "Happy, Anxious, Grateful, Sad, Excited, Calm, "
                        "Reflective, or Angry)."
                    ),
                },
                {
                    "role": "user",
                    "content": content,
                },
            ],
            temperature=0.4,
            max_completion_tokens=200,
            response_format={"type": "json_object"},
        )

        response_text = chat_completion.choices[0].message.content
        result = json.loads(response_text)

        return {
            'summary': result.get('summary', 'Unable to analyze'),
            'emotion': result.get('emotion', 'Neutral'),
        }

    except Exception as e:
        logger.error(f"Groq API error: {e}")
        return {
            'summary': 'Unable to analyze at this time.',
            'emotion': 'Neutral',
        }


@login_required
def dashboard(request):
    entries = DiaryEntry.objects.filter(user=request.user)
    return render(request, 'diary/dashboard.html', {'entries': entries})


@login_required
def entry_detail(request, pk):
    entry = get_object_or_404(DiaryEntry, pk=pk, user=request.user)
    return render(request, 'diary/entry_detail.html', {'entry': entry})


@login_required
def entry_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        summary = request.POST.get('summary', '')
        emotion = request.POST.get('emotion', '')
        entry = DiaryEntry.objects.create(
            user=request.user,
            title=title,
            content=content,
            summary=summary,
            emotion=emotion,
        )
        return redirect('entry_detail', pk=entry.pk)
    return render(request, 'diary/entry_form.html')


@login_required
def entry_update(request, pk):
    entry = get_object_or_404(DiaryEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        entry.title = request.POST.get('title')
        entry.content = request.POST.get('content')
        entry.summary = request.POST.get('summary', '')
        entry.emotion = request.POST.get('emotion', '')
        entry.save()
        return redirect('entry_detail', pk=entry.pk)
    return render(request, 'diary/entry_form.html', {'entry': entry})


@login_required
@require_POST
def entry_delete(request, pk):
    entry = get_object_or_404(DiaryEntry, pk=pk, user=request.user)
    entry.delete()
    return JsonResponse({'success': True})


@login_required
@require_POST
def analyze_entry_by_id(request, pk):
    # Process entry analysis and cache to DB
    entry = get_object_or_404(DiaryEntry, pk=pk, user=request.user)

    # Skip API call if insights already exist
    if entry.summary and entry.summary.strip():
        return JsonResponse({
            'summary': entry.summary,
            'emotion': entry.emotion,
            'cached': True,
        })

    insights = get_ai_insights(entry.content)
    
    # Cache and persist result
    entry.summary = insights['summary']
    entry.emotion = insights['emotion']
    entry.save(update_fields=['summary', 'emotion'])

    return JsonResponse({
        'summary': insights['summary'],
        'emotion': insights['emotion'],
        'cached': False,
    })


@login_required
@require_POST
def analyze_entry(request):
    # Fallback endpoint for new entry analysis
    data = json.loads(request.body)
    content = data.get('content', '')

    insights = get_ai_insights(content)

    return JsonResponse({
        'summary': insights['summary'],
        'emotion': insights['emotion'],
    })
