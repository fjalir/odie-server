from django.db import models

class Permission(models.Model):
    id = models.IntegerField(db_column='rechteid', primary_key=True)
    name = models.CharField(db_column='rechtename', max_length=32)

    class Meta:
        db_table = 'acl\".\"rechte'
        managed = False

class User(models.Model):
    id = models.IntegerField(db_column='benutzer_id', primary_key=True)
    username = models.CharField(db_column='benutzername', unique=True, max_length=255, blank=True)
    first_name = models.TextField(db_column='vorname')
    last_name = models.TextField(db_column='nachname')
    pw_hash = models.CharField(db_column='passwort', max_length=255)
    unix_uid = models.IntegerField()
    effective_permissions = models.ManyToManyField(Permission, through='EffectivePermissions')

    def is_authenticated(self):
        return True

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.username

    def has_permission(self, perm_name):
        return self.effective_permissions.filter(name=perm_name).exists()

    last_login = None
    def save(self, **kwargs):
        # ignore, used only for setting last_login
        pass

    REQUIRED_FIELDS = []  # not used, still necessary
    USERNAME_FIELD = 'username'
    class Meta:
        db_table = 'benutzer'
        managed = False

class EffectivePermissions(models.Model):
    user = models.ForeignKey(User, db_column='benutzer_id')
    permission = models.ForeignKey(Permission, db_column='rechteid')

    class Meta:
        db_table = 'acl\".\"effektive_benutzer_rechte'
        managed = False
