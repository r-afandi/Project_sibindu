# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class About(models.Model):
    id = models.BigAutoField(primary_key=True)
    nama = models.CharField(max_length=50)
    maps = models.TextField()
    tentang = models.TextField()
    tentang_footer = models.TextField()
    kontak = models.TextField()
    created_at = models.DateTimeField()
    update_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'about'


class Artikel(models.Model):
    id = models.BigAutoField(primary_key=True)
    judul = models.CharField(max_length=50, blank=True, null=True)
    tanggal = models.CharField(max_length=50, blank=True, null=True)
    artikel = models.TextField()
    img = models.CharField(max_length=100, blank=True, null=True)
    info = models.CharField(max_length=50, blank=True, null=True)
    validasi = models.CharField(max_length=50, blank=True, null=True)
    validator_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    update_at = models.DateTimeField(blank=True, null=True)
    delete_at = models.DateTimeField(blank=True, null=True)
    petugas_id = models.IntegerField(blank=True, null=True)
    upload = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'artikel'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DataPakar(models.Model):
    umur = models.CharField(max_length=20, blank=True, null=True)
    data_gejala = models.TextField(blank=True, null=True)
    data_luar = models.TextField(blank=True, null=True)
    data_dalam = models.TextField(blank=True, null=True)
    diagnosa_id = models.BigIntegerField()
    created_at = models.DateTimeField()
    update_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'data_pakar'


class DataSdp(models.Model):
    nama = models.CharField(max_length=50)
    kode = models.CharField(max_length=50)
    status_id = models.BigIntegerField(blank=True, null=True)
    info = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    update_at = models.DateTimeField(blank=True, null=True)
    delete_at = models.DateTimeField(blank=True, null=True)
    satuan = models.CharField(max_length=50, blank=True, null=True)
    jumlah_keluar = models.CharField(max_length=50, blank=True, null=True)
    jumlah_masuk = models.CharField(max_length=50, blank=True, null=True)
    kadaluarsa = models.CharField(max_length=50, blank=True, null=True)
    total = models.CharField(db_column='Total', max_length=50, blank=True, null=True)  # Field name made lowercase.
    produk = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_sdp'


class DataSuspek(models.Model):
    id = models.BigAutoField(primary_key=True)
    nama = models.TextField()
    no_ktp = models.CharField(max_length=16, blank=True, null=True)
    alamat = models.TextField()
    umur = models.CharField(max_length=3, blank=True, null=True)
    data_gejala = models.TextField(blank=True, null=True)
    data_dalam = models.TextField(blank=True, null=True)
    data_luar = models.TextField(blank=True, null=True)
    diagnosa_id = models.BigIntegerField(blank=True, null=True)
    penanganan = models.TextField()
    petugas_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_suspek'


class Diagnosa(models.Model):
    diagnosa = models.CharField(max_length=20)
    data_gejala = models.TextField(blank=True, null=True)
    data_dalam = models.TextField(blank=True, null=True)
    data_luar = models.TextField(blank=True, null=True)
    penanganan = models.TextField()
    created_at = models.DateTimeField()
    update_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'diagnosa'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoDrfFilepondStoredupload(models.Model):
    upload_id = models.CharField(primary_key=True, max_length=22)
    file = models.CharField(max_length=2048)
    uploaded = models.DateTimeField()
    stored = models.DateTimeField()
    uploaded_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_drf_filepond_storedupload'


class DjangoDrfFilepondTemporaryupload(models.Model):
    upload_id = models.CharField(primary_key=True, max_length=22)
    file = models.CharField(max_length=100)
    upload_name = models.CharField(max_length=512)
    uploaded = models.DateTimeField()
    upload_type = models.CharField(max_length=1)
    file_id = models.CharField(max_length=22)
    uploaded_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_drf_filepond_temporaryupload'


class DjangoDrfFilepondTemporaryuploadchunked(models.Model):
    upload_id = models.CharField(primary_key=True, max_length=22)
    file_id = models.CharField(max_length=22)
    upload_dir = models.CharField(max_length=512)
    last_chunk = models.IntegerField()
    total_size = models.BigIntegerField()
    upload_name = models.CharField(max_length=512)
    upload_complete = models.IntegerField()
    last_upload_time = models.DateTimeField()
    uploaded_by = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    offset = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'django_drf_filepond_temporaryuploadchunked'


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Dump(models.Model):
    nama = models.TextField()
    usia = models.CharField(max_length=3)
    gejala = models.TextField()
    img = models.CharField(max_length=100, blank=True, null=True)
    diagnosa_id = models.BigIntegerField(blank=True, null=True)
    petugas_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dump'


class FilepondUpload(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()
    original = models.CharField(max_length=100)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'filepond_upload'


class Gejala(models.Model):
    id = models.BigAutoField(primary_key=True)
    alias = models.TextField(blank=True, null=True)
    jenis = models.TextField(blank=True, null=True)
    rule_id = models.BigIntegerField(blank=True, null=True)
    pernyataan = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    update_at = models.DateTimeField()
    nama = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gejala'


class Kriteria(models.Model):
    id = models.BigAutoField(primary_key=True)
    nama = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField()
    update_at = models.DateTimeField(blank=True, null=True)
    badge = models.CharField(max_length=50, blank=True, null=True)
    kriteria = models.TextField(blank=True, null=True)
    apper = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kriteria'


class LaporanKegiatan(models.Model):
    id = models.BigAutoField(primary_key=True)
    nama = models.CharField(max_length=50)
    tanggal = models.CharField(max_length=50)
    kegiatan = models.TextField()
    img = models.CharField(max_length=100, blank=True, null=True)
    validasi = models.CharField(max_length=50, blank=True, null=True)
    info = models.CharField(max_length=50, blank=True, null=True)
    validator_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    delete_at = models.DateTimeField(blank=True, null=True)
    petugas_id = models.IntegerField(blank=True, null=True)
    upload = models.CharField(max_length=50, blank=True, null=True)
    update_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'laporan_kegiatan'


class LaporanSdp(models.Model):
    id = models.BigAutoField(primary_key=True)
    nama = models.CharField(max_length=50)
    jenis_id = models.BigIntegerField(blank=True, null=True)
    masuk = models.CharField(max_length=50)
    keluar = models.CharField(max_length=50)
    tanggal = models.CharField(max_length=50)
    validasi_id = models.CharField(max_length=50)
    info = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    update_at = models.DateTimeField(blank=True, null=True)
    delete_at = models.DateTimeField(blank=True, null=True)
    upload = models.CharField(max_length=250, blank=True, null=True)
    petugas_id = models.IntegerField(blank=True, null=True)
    validator_id = models.IntegerField(blank=True, null=True)
    keperluan = models.CharField(max_length=250, blank=True, null=True)
    bukti = models.CharField(max_length=100, blank=True, null=True)
    kadaluarsa = models.CharField(max_length=50, blank=True, null=True)
    kondisi_id = models.BigIntegerField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'laporan_sdp'


class Menu(models.Model):
    id = models.BigAutoField(primary_key=True)
    nama = models.TextField()
    link = models.TextField()
    icon = models.CharField(max_length=40)
    group = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menu'


class MenuDiagnosaPenanganan(models.Model):
    id = models.BigAutoField(primary_key=True)
    nama = models.TextField(blank=True, null=True)
    link = models.TextField()
    level = models.CharField(max_length=30)
    is_staff = models.CharField(max_length=30, blank=True, null=True)
    inisial = models.TextField(blank=True, null=True)
    link_view = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menu_diagnosa_penanganan'


class MenuGeneral(models.Model):
    id = models.BigAutoField(primary_key=True)
    nama = models.TextField()
    link = models.TextField()
    level = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menu_general'


class Pengumuman(models.Model):
    id = models.BigAutoField(primary_key=True)
    judul = models.CharField(max_length=50)
    tanggal = models.CharField(max_length=50)
    pengumuman = models.TextField()
    petugas_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    update_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'pengumuman'
