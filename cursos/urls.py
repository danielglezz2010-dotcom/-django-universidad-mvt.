from django.urls import path
from . import views

urlpatterns = [
    # Rutas antiguas (las usa lista.html con 'detalle_curso')
    path('', views.CursoListView.as_view(), name='lista_cursos'),
    path('curso/<int:pk>/', views.CursoDetailView.as_view(), name='detalle_curso'),
    path('profesor/<int:pk>/', views.ProfesorDetailView.as_view(), name='detalle_profesor'),
    path('profesores/', views.ProfesorListView.as_view(), name='lista_profesores'),
    path('profesor/<int:pk>/editar/', views.ProfesorUpdateView.as_view(), name='editar_profesor'),
    path('profesor/<int:pk>/eliminar/', views.ProfesorDeleteView.as_view(), name='eliminar_profesor'),

    # Rutas web con CBV
    path('web/cursos/', views.CursoListView.as_view(), name='web_lista_cursos'),
    path('web/cursos/<int:pk>/', views.CursoDetailView.as_view(), name='web_detalle_curso'),
    path('web/cursos/nuevo/', views.CursoCreateView.as_view(), name='web_crear_curso'),
    path('web/cursos/<int:pk>/editar/', views.CursoUpdateView.as_view(), name='web_editar_curso'),
    path('web/cursos/<int:pk>/eliminar/', views.CursoDeleteView.as_view(), name='web_eliminar_curso'),

    # ... rutas anteriores ...
    path('web/estudiantes/', views.EstudianteListView.as_view(), name='web_lista_estudiantes'),
    path('web/estudiantes/<int:pk>/', views.EstudianteDetailView.as_view(), name='web_detalle_estudiante'),
    path('web/estudiantes/nuevo/', views.EstudianteCreateView.as_view(), name='web_crear_estudiante'),
    path('web/estudiantes/<int:pk>/editar/', views.EstudianteUpdateView.as_view(), name='web_editar_estudiante'),
    path('web/estudiantes/<int:pk>/eliminar/', views.EstudianteDeleteView.as_view(), name='web_eliminar_estudiante'),


]

