import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Formation, PlayerPosition


def pitch_view(request):
    return render(request, 'tactics/pitch.html')


@csrf_exempt
def save_formation(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    data = json.loads(request.body)
    name = data.get('name', '').strip()
    players = data.get('players', [])

    if not name:
        return JsonResponse({'error': 'Formation name is required'}, status=400)
    if not players:
        return JsonResponse({'error': 'At least one player must be placed'}, status=400)

    formation = Formation.objects.create(name=name)
    for p in players:
        PlayerPosition.objects.create(
            formation=formation,
            label=str(p.get('number', '')),
            x=p['x'],
            y=p['y']
        )

    return JsonResponse({'success': True, 'formation_id': formation.id})




def formation_list(request):
    formations = Formation.objects.all().order_by('-created_at')
    return render(request, 'tactics/formation_list.html', {'formations': formations})


def load_formation(request, formation_id):
    try:
        formation = Formation.objects.get(id=formation_id)
    except Formation.DoesNotExist:
        return JsonResponse({'error': 'Formation not found'}, status=404)

    players = [
        {'number': p.label, 'x': p.x, 'y': p.y}
        for p in formation.positions.all()
    ]
    return JsonResponse({'name': formation.name, 'players': players})