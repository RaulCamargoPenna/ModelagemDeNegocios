from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Roles(models.Model):
    name = models.CharField(max_length=100, unique=True)
    role_permissions = models.ManyToManyField(
        Permission,
        related_name='roles_permissions',
        blank=True,
        help_text='Permissoes do cargo.',
    )
    
    def get_role_permissions(self):
        """
            Retorna o conjunto de permissões associadas ao cargo (role).
        """
        if self.cargo:
            return self.cargo.role_permissions.all()
        return []

    def get_user_permissions(self, obj=None):
        """
            Retorna permissões do usuário + permissões herdadas do cargo.
        """
        perms = super().get_user_permissions(obj)
        role_perms = self.get_role_permissions()
        role_perms_codenames = set(f"{p.content_type.app_label}.{p.codename}" for p in role_perms)
        return perms.union(role_perms_codenames)

    def get_all_permissions(self, obj=None):
        """
            Junta permissões do usuário, do grupo e do cargo.
        """
        all_perms = super().get_all_permissions(obj)
        role_perms = self.get_role_permissions()
        role_perms_codenames = set(f"{p.content_type.app_label}.{p.codename}" for p in role_perms)
        return all_perms.union(role_perms_codenames)

    def has_perm(self, perm, obj=None):
        """
            Verifica se o usuário tem a permissão, considerando as herdadas do cargo.
        """
        return perm in self.get_all_permissions(obj)
    
    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    """_summary_
        Tabela de usuários personalizada, inclusão do setor e do campo de imagem.
    """
    # Precisei alterar os related names pois estava conflitando com a outra tabela que havia sido criada.
    groups = models.ManyToManyField(
        Group,
        related_name='usuario_set',
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='usuario',
    )
    cargo = models.ForeignKey(Roles, on_delete=models.PROTECT, null=True)
    img_user = models.FileField(upload_to='media/users_img/', null=True, blank=True)
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',
        blank=True,
        help_text='Specific permissions for this user.'
    )
    
    def __str__(self):
        return self.username