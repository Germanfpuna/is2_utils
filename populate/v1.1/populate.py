from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from Pagina_CMS.models import Categoria, Articulo
from django.utils import timezone

class Command(BaseCommand):
    help = 'Crea un usuario con todos los permisos y que esté en todos los grupos, además de crear 3 categorías y 6 artículos con distintos estados'

    def handle(self, *args, **kwargs):
        # Crear usuario
        user, created = User.objects.get_or_create(username='user1', defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True})
        if created:
            user.set_password('1234')
            user.save()
            self.stdout.write(self.style.SUCCESS('Usuario user1 creado con éxito'))
        else:
            self.stdout.write(self.style.WARNING('Usuario user1 ya existe'))
            # Crear usuarios adicionales sin permisos ni grupos
            for username in ['user2', 'user3']:
                user, created = User.objects.get_or_create(username=username, defaults={'email': f'{username}@example.com'})
                if created:
                    user.set_password('1234')
                    user.save()
                    self.stdout.write(self.style.SUCCESS(f'Usuario {username} creado con éxito'))
                else:
                    self.stdout.write(self.style.WARNING(f'Usuario {username} ya existe'))

        # Asignar todos los permisos al usuario
        permissions = Permission.objects.all()
        user.user_permissions.set(permissions)
        self.stdout.write(self.style.SUCCESS('Todos los permisos asignados al usuario user1'))

        # Asignar usuario a todos los grupos
        groups = Group.objects.all()
        user.groups.set(groups)
        self.stdout.write(self.style.SUCCESS('Usuario user1 asignado a todos los grupos'))

        # Crear categorías
        categorias = [
            {'nombre': 'Categoría 1', 'moderado': False, 'es_pago': False, 'nivel_acceso': 'publico'},
            {'nombre': 'Categoría 2', 'moderado': True, 'es_pago': True, 'nivel_acceso': 'suscriptor', 'precio': 10.00},
            {'nombre': 'Categoría 3', 'moderado': False, 'es_pago': False, 'nivel_acceso': 'publico'}
        ]
        for cat_data in categorias:
            Categoria.objects.get_or_create(**cat_data)
        self.stdout.write(self.style.SUCCESS('3 categorías creadas con éxito'))

        # Crear artículos
        
        categorias = Categoria.objects.all()
        for i in range(6):
            Articulo.objects.create(
                titulo=f'Artículo {i+1}',
                art_de_pago=False,
                resumen=f'Resumen del artículo {i+1}',
                contenido=f'Contenido del artículo {i+1}',
                categoria=categorias[i % len(categorias)],
                estado='publicado',
                autor=user,
                tag=f'Tag {i+1}',
                fecha_publicado=timezone.now() - timezone.timedelta(days=1),
                fecha_fin=timezone.now() + timezone.timedelta(days=365)
            )
        self.stdout.write(self.style.SUCCESS('6 artículos creados con éxito'))