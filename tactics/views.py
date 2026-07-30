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
    arrows = data.get('arrows', [])
    ball = data.get('ball')  # { x, y } or null

    if not name:
        return JsonResponse({'error': 'Formation name is required'}, status=400)
    if not players:
        return JsonResponse({'error': 'At least one player must be placed'}, status=400)

    formation = Formation.objects.create(
        name=name,
        ball_x=ball['x'] if ball else None,
        ball_y=ball['y'] if ball else None
    )
    for p in players:
        PlayerPosition.objects.create(
            formation=formation,
            team=p.get('team', 'home'),
            label=str(p.get('number', '')),
            x=p['x'],
            y=p['y']
        )
    for a in arrows:
        MovementArrow.objects.create(
            formation=formation,
            start_x=a['startX'],
            start_y=a['startY'],
            end_x=a['endX'],
            end_y=a['endY']
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
        {'number': p.label, 'x': p.x, 'y': p.y, 'team': p.team}
        for p in formation.positions.all()
    ]
    arrows = [
        {'startX': a.start_x, 'startY': a.start_y, 'endX': a.end_x, 'endY': a.end_y}
        for a in formation.arrows.all()
    ]
    ball = None
    if formation.ball_x is not None and formation.ball_y is not None:
        ball = {'x': formation.ball_x, 'y': formation.ball_y}

    return JsonResponse({'name': formation.name, 'players': players, 'arrows': arrows, 'ball': ball})

@csrf_exempt
def delete_formation(request, formation_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        formation = Formation.objects.get(id=formation_id)
        formation.delete()
        return JsonResponse({'success': True})
    except Formation.DoesNotExist:
        return JsonResponse({'error': 'Formation not found'}, status=404)


@csrf_exempt
def rename_formation(request, formation_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    data = json.loads(request.body)
    new_name = data.get('name', '').strip()
    if not new_name:
        return JsonResponse({'error': 'Name cannot be empty'}, status=400)

    try:
        formation = Formation.objects.get(id=formation_id)
        formation.name = new_name
        formation.save()
        return JsonResponse({'success': True})
    except Formation.DoesNotExist:
        return JsonResponse({'error': 'Formation not found'}, status=404)