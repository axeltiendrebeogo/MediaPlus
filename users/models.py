from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """Manager personnalisé — l'email est l'identifiant de connexion (pas de username)."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", User.Role.GESTIONNAIRE)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        # Le superuser Django (accès /admin/) est toujours côté "admin" métier.
        extra_fields.setdefault("role", User.Role.ADMIN)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("nom", "Administrateur")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Le superuser doit avoir is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Le superuser doit avoir is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Modèle utilisateur — §4.1 du Cahier des Charges.

    NB : le champ `media_id` qui apparaît dans les réponses API (login,
    /auth/me/, etc.) n'est PAS stocké ici. Il est dérivé dynamiquement
    de Media.gestionnaire (relation inverse), car c'est le modèle Media
    qui porte la FK gestionnaire_id (§4.2 du CdC). Voir users/serializers.py.
    """

    class Role(models.TextChoices):
        ADMIN = "admin", "Administrateur"
        GESTIONNAIRE = "gestionnaire", "Gestionnaire Média"
        CONTROLEUR = "controleur", "Contrôleur Média"

    id = models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices)
    date_creation = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # Requis par Django pour l'accès à /admin/ — distinct du rôle métier.
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nom", "role"]

    class Meta:
        db_table = "users_user"
        ordering = ["nom"]

    def __str__(self):
        return f"{self.nom} ({self.email}) — {self.role}"

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_gestionnaire(self):
        return self.role == self.Role.GESTIONNAIRE

    @property
    def is_controleur(self):
        return self.role == self.Role.CONTROLEUR

    def get_media(self):
        """Retourne le Media dont cet utilisateur est gestionnaire, ou None."""
        if self.role != self.Role.GESTIONNAIRE:
            return None
        from medias.models import Media  # import différé — évite le cycle users <-> medias

        return Media.objects.filter(gestionnaire_id=self.id).first()
