from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import AppointmentForm
from .models import Institute
def institutes(request):
    return render(request, 'beauty/institutes.html', {'institutes':Institute.objects.filter(is_active=True).prefetch_related('services')})
@login_required
def book(request, slug):
    institute = get_object_or_404(Institute, slug=slug, is_active=True)
    form = AppointmentForm(request.POST or None, institute=institute)
    if request.method == 'POST' and form.is_valid():
        appointment = form.save(commit=False); appointment.client = request.user; appointment.save()
        messages.success(request, 'Votre demande de rendez-vous a été envoyée à l’institut.'); return redirect('institutes')
    return render(request, 'beauty/book.html', {'institute':institute, 'form':form})
