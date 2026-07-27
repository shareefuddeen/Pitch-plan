from django.shortcuts import render


def pitch_view(request):
    return render(request, 'tactics/pitch.html')