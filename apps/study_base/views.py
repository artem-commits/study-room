from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RoomForm
from .models import Room, Topic, Message
from django.views import generic
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class HomeListView(generic.ListView):
    """Display a list of rooms with search functionality and sidebar topics."""
    model = Room
    context_object_name = "rooms"
    template_name = "study_base/index.html"
    paginate_by = 5

    def get_queryset(self):
        """Filter rooms based on search query."""
        queryset = super().get_queryset()
        search_query = self.request.GET.get("q", "").strip()

        if (search_query is not None) and (search_query != ''):
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(topic__name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        """Add topics to context for sidebar."""
        queryset = super().get_queryset()
        search_query = self.request.GET.get("q", "").strip()
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['topics'] = Topic.objects.get_queryset()[:10]
        
        # Получаем все сообщения, если есть поисковый запрос, фильтруем по нему
        if search_query:
            context['room_messages'] = Message.objects.filter(
                Q(room__name__icontains=search_query) |
                Q(room__topic__name__icontains=search_query) |
                Q(body__icontains=search_query)
            )
        else:
            context['room_messages'] = Message.objects.all()
            
        return context


class RoomCreateView(LoginRequiredMixin, generic.CreateView):
    """Create a new room with authorization requirement."""
    model = Room
    template_name = 'study_base/room_form.html'
    form_class = RoomForm
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        form.instance.host = self.request.user
        return super().form_valid(form)


class RoomUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Update the room with authorization requirement."""
    model = Room
    template_name = 'study_base/room_form.html'
    form_class = RoomForm
    success_url = reverse_lazy('homepage')
    pk_url_kwarg = 'room_id'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.host != self.request.user:
            raise PermissionDenied("You don't have permission to edit this room.")
        return obj


class RoomDetailView(generic.View):
    """Create a new comment and detail view of all room."""

    def get(self, request, *args, **kwargs):
        room = get_object_or_404(Room, id=kwargs['room_id'])
        room_messages = room.message_set.get_queryset()
        participants = room.participants.all()
        return render(request, 'study_base/room.html', {
            'room': room,
            'room_messages': room_messages,
            'participants': participants,
        })

    def post(self, request, *args, **kwargs):
        room = get_object_or_404(Room, id=kwargs['room_id'])
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect('room', room_id=room.id)


class RoomDelete(LoginRequiredMixin, generic.DeleteView):
    model = Room
    template_name = 'study_base/delete.html'
    success_url = reverse_lazy('homepage')

    def get_object(self, queryset=None, **kwargs):
        return get_object_or_404(Room, id=self.kwargs['room_id'])


class MessageDelete(LoginRequiredMixin, generic.DeleteView):
    model = Message
    template_name = 'study_base/delete.html'
    success_url = reverse_lazy('homepage')

    def get_object(self, queryset=None, **kwargs):
        return get_object_or_404(Message, id=self.kwargs['id'])


class AboutView(generic.TemplateView):
    template_name = 'study_base/about.html'


class UserProfile(generic.TemplateView):
    template_name = 'study_base/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_user_model().objects.get(id=self.kwargs['pk'])
        context['user'] = user
        context['rooms'] = user.room_set.all()
        context['room_messages'] = user.message_set.all()
        context['topics'] = Topic.objects.get_queryset()
        return context


