from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Curso, Profesor, Estudiante
from .forms import CursoForm
from django.contrib.auth.views import LoginView
from .models import Estudiante
from .forms import EstudianteForm
from django.db.models import Q
from django.views.generic import ListView
from .models import Curso


class CursoListView(ListView):
    model = Curso
    paginate_by = 3
    ordering = ['nombre']
    template_name = 'cursos/lista.html'
    context_object_name = 'cursos'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '')
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(codigo__icontains=query) |
                Q(profesor__nombre__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['total_cursos'] = Curso.objects.count()
        return context



class CursoDetailView(DetailView):
    model = Curso
    template_name = 'cursos/detalle.html'
    context_object_name = 'curso'


class EstudianteListView(ListView):
    model = Estudiante
    template_name = 'cursos/estudiantes_lista.html'
    context_object_name = 'estudiantes'
    paginate_by = 5
    ordering = ['nombre']

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '')
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(matricula__icontains=query) |
                Q(email__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context
    


class EstudianteDetailView(DetailView):
    model = Estudiante
    template_name = 'cursos/estudiante_detalle.html'
    context_object_name = 'estudiante'


class ProfesorListView(ListView):
    model = Profesor     
    paginate_by = 3
    ordering = ['nombre']
    template_name = 'cursos/profesores_lista.html'
    context_object_name = 'profesores'

class ProfesorUpdateView(LoginRequiredMixin, UpdateView):
    model = Profesor
    fields = ['nombre', 'email', 'especialidad']
    template_name = 'cursos/formulario.html'
    success_url = reverse_lazy('lista_profesores')


class ProfesorDeleteView(LoginRequiredMixin, DeleteView):
    model = Profesor
    template_name = 'cursos/curso_confirm_delete.html'
    success_url = reverse_lazy('lista_profesores')

    
class ProfesorDetailView(DetailView):
    model = Profesor
    template_name = 'cursos/profesor_detalle.html'
    context_object_name = 'profesor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cursos'] = self.object.cursos.all()  # relación inversa
        return context
        
    
def lista_profesores(request):
    profesores = Profesor.objects.all()
    return render(request, 'cursos/profesores_lista.html', {
        'profesores': profesores,
    })   
  # 1. Vista para CREAR un Curso (Manejo de GET y POST)
def crear_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            # Guarda automáticamente el curso y sus relaciones (FK y M2M)
            form.save()
            return redirect('web_lista_cursos')
    else:
        # Petición GET: Muestra el formulario vacío
        form = CursoForm()
    
    context = {'form': form, 'titulo': 'Crear Nuevo Curso'}
    return render(request, 'cursos/formulario.html', context)


# 2. Vista para EDITAR un Curso existente
def editar_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    
    if request.method == 'POST':
        # Pasamos instance=curso para que actualice en lugar de crear uno nuevo
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            return redirect('web_lista_cursos')
    else:
        # Petición GET: Muestra el formulario precargado con la información existente
        form = CursoForm(instance=curso)
    
    context = {'form': form, 'titulo': f'Editar Curso: {curso.nombre}'}
    return render(request, 'cursos/formulario.html', context)


class CursoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Curso
    form_class = CursoForm 
    template_name = 'cursos/formulario.html'
    success_url = reverse_lazy('web_lista_cursos')
    success_message = "¡El curso '%(nombre)s' fue creado exitosamente!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Nuevo Curso (Protegido)'
        return context



class CursoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Curso
    form_class = CursoForm 
    template_name = 'cursos/formulario.html'
    success_url = reverse_lazy('web_lista_cursos')
    success_message = "¡El curso '%(nombre)s' fue actualizado correctamente!"



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Curso: {self.object.nombre}'
        return context



class CursoDeleteView(LoginRequiredMixin, DeleteView):
    model = Curso
    template_name = 'cursos/curso_confirm_delete.html'
    success_url = reverse_lazy('web_lista_cursos')

    def form_valid(self, form):
        messages.warning(self.request, f"El curso '{self.object.nombre}' fue eliminado del sistema.")
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        messages.info(self.request, f"¡Bienvenido de nuevo, {form.get_user().username}!")
        return super().form_valid(form)


class EstudianteCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'cursos/estudiante_formulario.html'
    success_url = reverse_lazy('web_lista_estudiantes')
    success_message = "¡El estudiante '%(nombre)s' fue registrado con éxito!"


class EstudianteUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'cursos/estudiante_formulario.html'
    success_url = reverse_lazy('web_lista_estudiantes')
    success_message = "¡Los datos del estudiante '%(nombre)s' fueron actualizados correctamente!"


class EstudianteDeleteView(LoginRequiredMixin, DeleteView):
    model = Estudiante
    template_name = 'cursos/estudiante_confirm_delete.html'
    success_url = reverse_lazy('web_lista_estudiantes')
    context_object_name = 'estudiante'

    def form_valid(self, form):
        messages.warning(self.request, f"El estudiante '{self.object.nombre}' fue eliminado.")
        return super().form_valid(form) 
