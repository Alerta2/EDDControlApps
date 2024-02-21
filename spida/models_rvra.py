# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Canales(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='NOMBRE', max_length=45, blank=True, null=True)  # Field name made lowercase.
    unidades = models.CharField(db_column='UNIDADES', max_length=20, blank=True, null=True)  # Field name made lowercase.
    factor = models.FloatField(db_column='FACTOR', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'canales'


class ConfigEstacionWebrarex(models.Model):
    id_estacion = models.IntegerField(db_column='ID_ESTACION', primary_key=True)  # Field name made lowercase.
    id_detector = models.IntegerField(db_column='ID_DETECTOR')  # Field name made lowercase.
    tipo_detector = models.CharField(db_column='TIPO_DETECTOR', max_length=30)  # Field name made lowercase.
    isotopo = models.IntegerField(db_column='ISOTOPO')  # Field name made lowercase.
    decimales = models.IntegerField(db_column='DECIMALES')  # Field name made lowercase.
    unidades = models.CharField(db_column='UNIDADES', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'config_estacion_webrarex'
        unique_together = (('id_estacion', 'id_detector', 'isotopo'),)


class ConfigGraficasRare(models.Model):
    id_boton = models.IntegerField()
    nombre_boton = models.CharField(max_length=90, blank=True, null=True)
    id_subseccion = models.IntegerField()
    nombre_subseccion = models.CharField(max_length=90, blank=True, null=True)
    id_estacion = models.IntegerField()
    detector = models.IntegerField(blank=True, null=True)
    series = models.CharField(max_length=200, blank=True, null=True)
    tamanio = models.IntegerField(blank=True, null=True)
    dias = models.IntegerField(blank=True, null=True)
    red = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'config_graficas_rare'


class ConfigMonitoriza(models.Model):
    estacion = models.OneToOneField('Estaciones', models.DO_NOTHING, db_column='ESTACION_ID', primary_key=True)  # Field name made lowercase.
    can_det_est = models.IntegerField(db_column='CAN_DET_EST')  # Field name made lowercase.
    isotopo = models.ForeignKey('Isotopos', models.DO_NOTHING, db_column='ISOTOPO_ID')  # Field name made lowercase.
    csn = models.IntegerField(db_column='CSN', blank=True, null=True)  # Field name made lowercase.
    min_sd_csn = models.IntegerField(db_column='MIN_SD_CSN', blank=True, null=True)  # Field name made lowercase.
    csn_f_ult_valor = models.DateTimeField(db_column='CSN_F_ULT_VALOR', blank=True, null=True)  # Field name made lowercase.
    sd_activo = models.IntegerField(db_column='SD_ACTIVO', blank=True, null=True)  # Field name made lowercase.
    minutos_sd = models.IntegerField(db_column='MINUTOS_SD', blank=True, null=True)  # Field name made lowercase.
    f_ini_sin_datos = models.DateTimeField(db_column='F_INI_SIN_DATOS', blank=True, null=True)  # Field name made lowercase.
    sd_sms_env = models.IntegerField(db_column='SD_SMS_ENV', blank=True, null=True)  # Field name made lowercase.
    med_anio_ant = models.FloatField(db_column='MED_ANIO_ANT', blank=True, null=True)  # Field name made lowercase.
    med_amd_anio_ant = models.FloatField(db_column='MED_AMD_ANIO_ANT', blank=True, null=True)  # Field name made lowercase.
    niveles_activo = models.IntegerField(db_column='NIVELES_ACTIVO', blank=True, null=True)  # Field name made lowercase.
    sms_enviado = models.IntegerField(db_column='SMS_ENVIADO', blank=True, null=True)  # Field name made lowercase.
    f_ini_nivel = models.DateTimeField(db_column='F_INI_NIVEL', blank=True, null=True)  # Field name made lowercase.
    factor_n1 = models.FloatField(db_column='FACTOR_N1', blank=True, null=True)  # Field name made lowercase.
    factor_n2 = models.FloatField(db_column='FACTOR_N2', blank=True, null=True)  # Field name made lowercase.
    factor_n3 = models.FloatField(db_column='FACTOR_N3', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'config_monitoriza'
        unique_together = (('estacion', 'can_det_est', 'isotopo'),)


class ConfigSerieGrafica(models.Model):
    tipodato = models.CharField(db_column='tipoDato', max_length=30, blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=30, blank=True, null=True)
    eje = models.CharField(max_length=30, blank=True, null=True)
    ejemain = models.IntegerField(blank=True, null=True)
    tabla = models.CharField(max_length=30, blank=True, null=True)
    canal = models.IntegerField(blank=True, null=True)
    textoeje = models.CharField(db_column='textoEje', max_length=30, blank=True, null=True)  # Field name made lowercase.
    color = models.CharField(max_length=30, blank=True, null=True)
    tipografica = models.CharField(db_column='tipoGrafica', max_length=30, blank=True, null=True)  # Field name made lowercase.
    redondeo = models.IntegerField(blank=True, null=True)
    horasaviso = models.IntegerField(db_column='horasAviso', blank=True, null=True)  # Field name made lowercase.
    horasalerta = models.IntegerField(db_column='horasAlerta', blank=True, null=True)  # Field name made lowercase.
    horasincidencia = models.IntegerField(db_column='horasIncidencia', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'config_serie_grafica'


class ControlConexiones(models.Model):
    estacion = models.IntegerField(db_column='ESTACION', primary_key=True)  # Field name made lowercase.
    conexion = models.IntegerField(db_column='CONEXION')  # Field name made lowercase.
    fecha_hora = models.DateTimeField(db_column='FECHA_HORA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'control_conexiones'
        unique_together = (('estacion', 'conexion'),)


class ControlEstadoEstacion(models.Model):
    id_alertas = models.IntegerField(db_column='ID_ALERTAS', primary_key=True)  # Field name made lowercase.
    fecha_hora = models.DateTimeField(db_column='FECHA_HORA')  # Field name made lowercase.
    estaciones = models.ForeignKey('Estaciones', models.DO_NOTHING, db_column='ESTACIONES_ID')  # Field name made lowercase.
    mensaje = models.TextField(db_column='MENSAJE')  # Field name made lowercase.
    tipo = models.IntegerField(db_column='TIPO')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'control_estado_estacion'
        unique_together = (('id_alertas', 'fecha_hora', 'estaciones'),)


class DatosCorregidos(models.Model):
    id_datos_corregidos = models.IntegerField(primary_key=True)
    fecha_hora = models.DateTimeField()
    canal = models.IntegerField()
    estacion = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'datos_corregidos'


class DatosCorregidosGraficas(models.Model):
    usuario = models.CharField(max_length=90)
    fecha = models.DateTimeField()
    tabla = models.CharField(max_length=255)
    elemento = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'datos_corregidos_graficas'


class DatosMonitoriza(models.Model):
    estacion = models.OneToOneField('Estaciones', models.DO_NOTHING, db_column='ESTACION_ID', primary_key=True)  # Field name made lowercase.
    can_det_est = models.IntegerField(db_column='CAN_DET_EST')  # Field name made lowercase.
    isotopo = models.ForeignKey('Isotopos', models.DO_NOTHING, db_column='ISOTOPO_ID')  # Field name made lowercase.
    portugal = models.IntegerField(db_column='PORTUGAL', blank=True, null=True)  # Field name made lowercase.
    csn = models.IntegerField(db_column='CSN', blank=True, null=True)  # Field name made lowercase.
    min_sd_csn = models.IntegerField(db_column='MIN_SD_CSN', blank=True, null=True)  # Field name made lowercase.
    csn_f_ult_valor = models.DateTimeField(db_column='CSN_F_ULT_VALOR', blank=True, null=True)  # Field name made lowercase.
    sd_activo = models.IntegerField(db_column='SD_ACTIVO', blank=True, null=True)  # Field name made lowercase.
    minutos_sd = models.IntegerField(db_column='MINUTOS_SD', blank=True, null=True)  # Field name made lowercase.
    f_ini_sin_datos = models.DateTimeField(db_column='F_INI_SIN_DATOS', blank=True, null=True)  # Field name made lowercase.
    sd_sms_env = models.IntegerField(db_column='SD_SMS_ENV', blank=True, null=True)  # Field name made lowercase.
    med_anio_ant = models.FloatField(db_column='MED_ANIO_ANT', blank=True, null=True)  # Field name made lowercase.
    med_amd_anio_ant = models.FloatField(db_column='MED_AMD_ANIO_ANT', blank=True, null=True)  # Field name made lowercase.
    n1_activo = models.IntegerField(db_column='N1_ACTIVO', blank=True, null=True)  # Field name made lowercase.
    factor_n1 = models.FloatField(db_column='FACTOR_N1', blank=True, null=True)  # Field name made lowercase.
    f_i_niv_1 = models.DateTimeField(db_column='F_I_NIV_1', blank=True, null=True)  # Field name made lowercase.
    n1_sms_env = models.IntegerField(db_column='N1_SMS_ENV', blank=True, null=True)  # Field name made lowercase.
    n2_activo = models.IntegerField(db_column='N2_ACTIVO', blank=True, null=True)  # Field name made lowercase.
    factor_n2 = models.FloatField(db_column='FACTOR_N2', blank=True, null=True)  # Field name made lowercase.
    f_i_niv_2 = models.DateTimeField(db_column='F_I_NIV_2', blank=True, null=True)  # Field name made lowercase.
    n2_sms_env = models.IntegerField(db_column='N2_SMS_ENV', blank=True, null=True)  # Field name made lowercase.
    n3_activo = models.IntegerField(db_column='N3_ACTIVO', blank=True, null=True)  # Field name made lowercase.
    factor_n3 = models.FloatField(db_column='FACTOR_N3', blank=True, null=True)  # Field name made lowercase.
    f_i_niv_3 = models.DateTimeField(db_column='F_I_NIV_3', blank=True, null=True)  # Field name made lowercase.
    n3_sms_env = models.IntegerField(db_column='N3_SMS_ENV', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'datos_monitoriza'
        unique_together = (('estacion', 'can_det_est', 'isotopo'),)


class DatosMonitorizables(models.Model):
    estacion = models.OneToOneField('Estaciones', models.DO_NOTHING, db_column='ESTACION_ID', primary_key=True)  # Field name made lowercase.
    can_det_est = models.IntegerField(db_column='CAN_DET_EST')  # Field name made lowercase.
    isotopo = models.ForeignKey('Isotopos', models.DO_NOTHING, db_column='ISOTOPO_ID')  # Field name made lowercase.
    portugal = models.IntegerField(db_column='PORTUGAL', blank=True, null=True)  # Field name made lowercase.
    csn = models.IntegerField(db_column='CSN', blank=True, null=True)  # Field name made lowercase.
    min_sd_csn = models.IntegerField(db_column='MIN_SD_CSN', blank=True, null=True)  # Field name made lowercase.
    csn_f_ult_valor = models.DateTimeField(db_column='CSN_F_ULT_VALOR', blank=True, null=True)  # Field name made lowercase.
    sd_activo = models.IntegerField(db_column='SD_ACTIVO', blank=True, null=True)  # Field name made lowercase.
    minutos_sd = models.IntegerField(db_column='MINUTOS_SD', blank=True, null=True)  # Field name made lowercase.
    f_ini_sin_datos = models.DateTimeField(db_column='F_INI_SIN_DATOS', blank=True, null=True)  # Field name made lowercase.
    sd_sms_env = models.IntegerField(db_column='SD_SMS_ENV', blank=True, null=True)  # Field name made lowercase.
    med_anio_ant = models.FloatField(db_column='MED_ANIO_ANT', blank=True, null=True)  # Field name made lowercase.
    med_amd_anio_ant = models.FloatField(db_column='MED_AMD_ANIO_ANT', blank=True, null=True)  # Field name made lowercase.
    n1_activo = models.IntegerField(db_column='N1_ACTIVO', blank=True, null=True)  # Field name made lowercase.
    factor_n1 = models.FloatField(db_column='FACTOR_N1', blank=True, null=True)  # Field name made lowercase.
    f_i_niv_1 = models.DateTimeField(db_column='F_I_NIV_1', blank=True, null=True)  # Field name made lowercase.
    n1_sms_env = models.IntegerField(db_column='N1_SMS_ENV', blank=True, null=True)  # Field name made lowercase.
    n2_activo = models.IntegerField(db_column='N2_ACTIVO', blank=True, null=True)  # Field name made lowercase.
    factor_n2 = models.FloatField(db_column='FACTOR_N2', blank=True, null=True)  # Field name made lowercase.
    f_i_niv_2 = models.DateTimeField(db_column='F_I_NIV_2', blank=True, null=True)  # Field name made lowercase.
    n2_sms_env = models.IntegerField(db_column='N2_SMS_ENV', blank=True, null=True)  # Field name made lowercase.
    n3_activo = models.IntegerField(db_column='N3_ACTIVO', blank=True, null=True)  # Field name made lowercase.
    factor_n3 = models.FloatField(db_column='FACTOR_N3', blank=True, null=True)  # Field name made lowercase.
    f_i_niv_3 = models.DateTimeField(db_column='F_I_NIV_3', blank=True, null=True)  # Field name made lowercase.
    n3_sms_env = models.IntegerField(db_column='N3_SMS_ENV', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'datos_monitorizables'
        unique_together = (('estacion', 'can_det_est', 'isotopo'),)


class DescripcionTablas(models.Model):
    id_entrada = models.IntegerField(primary_key=True)
    nombre_tabla = models.CharField(max_length=100)
    descripcion_tabla = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'descripcion_tablas'


class Detectores(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='NOMBRE', max_length=30, blank=True, null=True)  # Field name made lowercase.
    unidades = models.CharField(db_column='UNIDADES', max_length=30, blank=True, null=True)  # Field name made lowercase.
    denom = models.CharField(db_column='DENOM', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'detectores'


class DispositivosMoviles(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_estacion = models.IntegerField(db_column='ID_ESTACION')  # Field name made lowercase.
    tipo = models.CharField(db_column='TIPO', max_length=20)  # Field name made lowercase.
    nombre = models.CharField(db_column='NOMBRE', max_length=20)  # Field name made lowercase.
    activo = models.IntegerField(db_column='ACTIVO', blank=True, null=True)  # Field name made lowercase.
    base_lat = models.FloatField(db_column='BASE_LAT', blank=True, null=True)  # Field name made lowercase.
    base_lon = models.FloatField(db_column='BASE_LON', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dispositivos_moviles'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Dosis(models.Model):
    id = models.BigAutoField(primary_key=True)
    idgeopos = models.ForeignKey('Geopos', models.DO_NOTHING, db_column='idgeopos', blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dosis'


class Esp3Minutos(models.Model):
    fecha_hora_inicial = models.DateTimeField(db_column='FECHA_HORA_INICIAL', primary_key=True)  # Field name made lowercase.
    relacion_detectores_estacion_id = models.IntegerField(db_column='RELACION_DETECTORES_ESTACION_ID')  # Field name made lowercase.
    tiempo_seg = models.IntegerField(db_column='TIEMPO_SEG', blank=True, null=True)  # Field name made lowercase.
    cnf = models.CharField(db_column='CNF', max_length=255, blank=True, null=True)  # Field name made lowercase.
    txt = models.CharField(db_column='TXT', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'esp_3_minutos'
        unique_together = (('fecha_hora_inicial', 'relacion_detectores_estacion_id'),)


class Espectros(models.Model):
    id = models.BigAutoField(primary_key=True)
    idgeopos = models.ForeignKey('Geopos', models.DO_NOTHING, db_column='idgeopos', blank=True, null=True)
    espectro = models.TextField(blank=True, null=True)
    filename = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'espectros'


class EspectrosAcumulados(models.Model):
    fecha_hora_inicial = models.DateTimeField(db_column='FECHA_HORA_INICIAL', primary_key=True)  # Field name made lowercase.
    relacion_detectores_estacion_id = models.IntegerField(db_column='RELACION_DETECTORES_ESTACION_ID')  # Field name made lowercase.
    tiempo_seg = models.IntegerField(db_column='TIEMPO_SEG', blank=True, null=True)  # Field name made lowercase.
    cnf = models.CharField(db_column='CNF', max_length=255, blank=True, null=True)  # Field name made lowercase.
    txt = models.CharField(db_column='TXT', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'espectros_acumulados'
        unique_together = (('fecha_hora_inicial', 'relacion_detectores_estacion_id'),)


class EspectrosDiarios(models.Model):
    fecha_hora_inicial = models.DateTimeField(db_column='FECHA_HORA_INICIAL', primary_key=True)  # Field name made lowercase.
    relacion_detectores_estacion_id = models.IntegerField(db_column='RELACION_DETECTORES_ESTACION_ID')  # Field name made lowercase.
    tiempo_seg = models.IntegerField(db_column='TIEMPO_SEG', blank=True, null=True)  # Field name made lowercase.
    cnf = models.CharField(db_column='CNF', max_length=255, blank=True, null=True)  # Field name made lowercase.
    txt = models.CharField(db_column='TXT', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'espectros_diarios'
        unique_together = (('fecha_hora_inicial', 'relacion_detectores_estacion_id'),)


class EstEspecGamma(models.Model):
    fecha_hora = models.DateTimeField(db_column='FECHA_HORA', primary_key=True)  # Field name made lowercase.
    relacion_detectores_estacion_id = models.IntegerField(db_column='RELACION_DETECTORES_ESTACION_ID')  # Field name made lowercase.
    isotopos_id = models.IntegerField(db_column='ISOTOPOS_ID')  # Field name made lowercase.
    actividad = models.FloatField(db_column='ACTIVIDAD', blank=True, null=True)  # Field name made lowercase.
    error = models.FloatField(db_column='ERROR', blank=True, null=True)  # Field name made lowercase.
    amd = models.FloatField(db_column='AMD', blank=True, null=True)  # Field name made lowercase.
    valido = models.IntegerField(db_column='VALIDO', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'est_espec_gamma'
        unique_together = (('fecha_hora', 'relacion_detectores_estacion_id', 'isotopos_id'),)


class EstEspecGammaAcumulados(models.Model):
    fecha_hora = models.DateTimeField(db_column='FECHA_HORA', primary_key=True)  # Field name made lowercase.
    relacion_detectores_estacion_id = models.IntegerField(db_column='RELACION_DETECTORES_ESTACION_ID')  # Field name made lowercase.
    isotopos_id = models.IntegerField(db_column='ISOTOPOS_ID')  # Field name made lowercase.
    actividad = models.FloatField(db_column='ACTIVIDAD', blank=True, null=True)  # Field name made lowercase.
    error = models.FloatField(db_column='ERROR', blank=True, null=True)  # Field name made lowercase.
    amd = models.FloatField(db_column='AMD', blank=True, null=True)  # Field name made lowercase.
    valido = models.IntegerField(db_column='VALIDO', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'est_espec_gamma_acumulados'
        unique_together = (('fecha_hora', 'relacion_detectores_estacion_id', 'isotopos_id'),)


class EstGamYRadioyodos(models.Model):
    fecha_hora = models.DateTimeField(db_column='FECHA_HORA', primary_key=True)  # Field name made lowercase.
    estaciones = models.ForeignKey('Estaciones', models.DO_NOTHING, db_column='ESTACIONES_ID')  # Field name made lowercase.
    canales = models.ForeignKey(Canales, models.DO_NOTHING, db_column='CANALES_ID')  # Field name made lowercase.
    valor = models.FloatField(db_column='VALOR', blank=True, null=True)  # Field name made lowercase.
    valido = models.IntegerField(db_column='VALIDO', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'est_gam_y_radioyodos'
        unique_together = (('fecha_hora', 'estaciones', 'canales'),)


class EstGamYRadioyodosAcumulados(models.Model):
    fecha_hora = models.DateTimeField(db_column='FECHA_HORA', primary_key=True)  # Field name made lowercase.
    estaciones = models.ForeignKey('Estaciones', models.DO_NOTHING, db_column='ESTACIONES_ID')  # Field name made lowercase.
    canales = models.ForeignKey(Canales, models.DO_NOTHING, db_column='CANALES_ID')  # Field name made lowercase.
    valor = models.FloatField(db_column='VALOR', blank=True, null=True)  # Field name made lowercase.
    valido = models.IntegerField(db_column='VALIDO', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'est_gam_y_radioyodos_acumulados'
        unique_together = (('fecha_hora', 'estaciones', 'canales'),)


class EstMeteorologicas(models.Model):
    fecha_hora = models.DateTimeField(db_column='FECHA_HORA', primary_key=True)  # Field name made lowercase.
    estaciones = models.ForeignKey('Estaciones', models.DO_NOTHING, db_column='ESTACIONES_ID')  # Field name made lowercase.
    canales = models.ForeignKey(Canales, models.DO_NOTHING, db_column='CANALES_ID')  # Field name made lowercase.
    valor = models.FloatField(db_column='VALOR', blank=True, null=True)  # Field name made lowercase.
    valido = models.IntegerField(db_column='VALIDO', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'est_meteorologicas'
        unique_together = (('fecha_hora', 'estaciones', 'canales'),)


class Estaciones(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='NOMBRE', max_length=45, blank=True, null=True)  # Field name made lowercase.
    map_lat = models.FloatField(db_column='MAP_LAT', blank=True, null=True)  # Field name made lowercase.
    map_lon = models.FloatField(db_column='MAP_LON', blank=True, null=True)  # Field name made lowercase.
    dir_fotos = models.CharField(db_column='DIR_FOTOS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    visualizar = models.IntegerField(db_column='VISUALIZAR', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'estaciones'


class Geopos(models.Model):
    id = models.BigAutoField(primary_key=True)
    idsesion = models.ForeignKey('Sesion', models.DO_NOTHING, db_column='idsesion', blank=True, null=True)
    fechahora = models.DateTimeField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    northing = models.CharField(max_length=1, blank=True, null=True)
    westing = models.CharField(max_length=1, blank=True, null=True)
    altitud = models.FloatField(blank=True, null=True)
    velocidad = models.FloatField(blank=True, null=True)
    idestacionmovil = models.IntegerField(db_column='idEstacionMovil', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'geopos'


class HistoricoTotalDatos(models.Model):
    dia = models.DateField(db_column='DIA', primary_key=True)  # Field name made lowercase.
    estacion = models.IntegerField(db_column='ESTACION')  # Field name made lowercase.
    can_det_est = models.IntegerField(db_column='CAN_DET_EST')  # Field name made lowercase.
    isotopo = models.IntegerField(db_column='ISOTOPO')  # Field name made lowercase.
    datos_radio = models.IntegerField(db_column='DATOS_RADIO', blank=True, null=True)  # Field name made lowercase.
    errores_radio = models.IntegerField(db_column='ERRORES_RADIO', blank=True, null=True)  # Field name made lowercase.
    intranet = models.IntegerField(db_column='INTRANET', blank=True, null=True)  # Field name made lowercase.
    recuperados = models.IntegerField(db_column='RECUPERADOS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'historico_total_datos'
        unique_together = (('dia', 'estacion', 'can_det_est', 'isotopo'),)


class Imagenes(models.Model):
    id = models.BigAutoField(primary_key=True)
    idgeopos = models.ForeignKey(Geopos, models.DO_NOTHING, db_column='idgeopos', blank=True, null=True)
    filename = models.TextField(blank=True, null=True)
    imagen = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'imagenes'


class Incidencias(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha_hora = models.DateTimeField(db_column='FECHA_HORA', blank=True, null=True)  # Field name made lowercase.
    estacion_id = models.IntegerField(db_column='ESTACION_ID', blank=True, null=True)  # Field name made lowercase.
    fecha_hora_apertura = models.DateTimeField(db_column='FECHA_HORA_APERTURA', blank=True, null=True)  # Field name made lowercase.
    fecha_hora_cierre = models.DateTimeField(db_column='FECHA_HORA_CIERRE', blank=True, null=True)  # Field name made lowercase.
    comentario_apertura = models.CharField(db_column='COMENTARIO_APERTURA', max_length=160, blank=True, null=True)  # Field name made lowercase.
    comentario_cierre = models.CharField(db_column='COMENTARIO_CIERRE', max_length=160, blank=True, null=True)  # Field name made lowercase.
    estado = models.IntegerField(db_column='ESTADO', blank=True, null=True)  # Field name made lowercase.
    usuario = models.CharField(db_column='USUARIO', max_length=50, blank=True, null=True)  # Field name made lowercase.
    enviado = models.IntegerField(db_column='ENVIADO')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'incidencias'


class InformacionesEstaciones(models.Model):
    id_estacion = models.OneToOneField(Estaciones, models.DO_NOTHING, db_column='ID_ESTACION', primary_key=True)  # Field name made lowercase.
    red = models.CharField(db_column='RED', max_length=30, blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='TIPO', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ubicacion_riesgo = models.IntegerField(db_column='UBICACION_RIESGO', blank=True, null=True)  # Field name made lowercase.
    angulo_riesgo = models.IntegerField(db_column='ANGULO_RIESGO', blank=True, null=True)  # Field name made lowercase.
    angulo_riesgo_min = models.IntegerField(db_column='ANGULO_RIESGO_MIN', blank=True, null=True)  # Field name made lowercase.
    angulo_riesgo_max = models.IntegerField(db_column='ANGULO_RIESGO_MAX', blank=True, null=True)  # Field name made lowercase.
    distancia = models.IntegerField(db_column='DISTANCIA', blank=True, null=True)  # Field name made lowercase.
    tiempo_consulta = models.IntegerField(db_column='TIEMPO_CONSULTA', blank=True, null=True)  # Field name made lowercase.
    zona = models.IntegerField(db_column='ZONA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'informaciones_estaciones'


class InformesConfirmados(models.Model):
    id_informes_confirmados = models.IntegerField(primary_key=True)
    id_usuario_informe = models.IntegerField()
    fecha_hora_informe = models.DateTimeField()
    id_usuario_vb = models.IntegerField()
    fecha_hora_confirmacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'informes_confirmados'


class InformesPendientesConfirmacion(models.Model):
    id_informes_pendientes_confirmacion = models.IntegerField(primary_key=True)
    id_usuario_informe = models.IntegerField()
    fecha_hora_informe = models.DateTimeField()
    id_usuario_vb = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'informes_pendientes_confirmacion'


class Isotopos(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    n_iso = models.CharField(db_column='N_ISO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    energia = models.FloatField(db_column='ENERGIA', blank=True, null=True)  # Field name made lowercase.
    c_izq = models.PositiveIntegerField(db_column='C_IZQ', blank=True, null=True)  # Field name made lowercase.
    c_der = models.PositiveIntegerField(db_column='C_DER', blank=True, null=True)  # Field name made lowercase.
    artificial = models.IntegerField(db_column='ARTIFICIAL', blank=True, null=True)  # Field name made lowercase.
    factor_nivel = models.FloatField(db_column='FACTOR_NIVEL', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'isotopos'


class MediasDiarias(models.Model):
    fecha = models.DateField(db_column='FECHA', primary_key=True)  # Field name made lowercase.
    id_estacion = models.ForeignKey(Estaciones, models.DO_NOTHING, db_column='ID_ESTACION')  # Field name made lowercase.
    id_detector = models.IntegerField(db_column='ID_DETECTOR')  # Field name made lowercase.
    id_canal = models.IntegerField(db_column='ID_CANAL')  # Field name made lowercase.
    valor = models.FloatField(db_column='VALOR', blank=True, null=True)  # Field name made lowercase.
    err = models.FloatField(db_column='ERR', blank=True, null=True)  # Field name made lowercase.
    amd = models.FloatField(db_column='AMD', blank=True, null=True)  # Field name made lowercase.
    n1 = models.IntegerField(db_column='N1', blank=True, null=True)  # Field name made lowercase.
    n2 = models.IntegerField(db_column='N2', blank=True, null=True)  # Field name made lowercase.
    n3 = models.IntegerField(db_column='N3', blank=True, null=True)  # Field name made lowercase.
    operatividad = models.FloatField(db_column='OPERATIVIDAD', blank=True, null=True)  # Field name made lowercase.
    total_datos = models.IntegerField(db_column='TOTAL_DATOS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'medias_diarias'
        unique_together = (('fecha', 'id_estacion', 'id_detector', 'id_canal'),)


class MediasDiariasCopy(models.Model):
    fecha = models.DateTimeField(db_column='FECHA', primary_key=True)  # Field name made lowercase.
    id_estacion = models.ForeignKey(Estaciones, models.DO_NOTHING, db_column='ID_ESTACION')  # Field name made lowercase.
    id_detector = models.IntegerField(db_column='ID_DETECTOR')  # Field name made lowercase.
    id_canal = models.IntegerField(db_column='ID_CANAL')  # Field name made lowercase.
    valor = models.FloatField(db_column='VALOR', blank=True, null=True)  # Field name made lowercase.
    err = models.FloatField(db_column='ERR', blank=True, null=True)  # Field name made lowercase.
    amd = models.FloatField(db_column='AMD', blank=True, null=True)  # Field name made lowercase.
    n1 = models.IntegerField(db_column='N1', blank=True, null=True)  # Field name made lowercase.
    n2 = models.IntegerField(db_column='N2', blank=True, null=True)  # Field name made lowercase.
    n3 = models.IntegerField(db_column='N3', blank=True, null=True)  # Field name made lowercase.
    operatividad = models.FloatField(db_column='OPERATIVIDAD', blank=True, null=True)  # Field name made lowercase.
    total_datos = models.IntegerField(db_column='TOTAL_DATOS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'medias_diarias_copy'
        unique_together = (('fecha', 'id_estacion', 'id_detector', 'id_canal'),)


class MediasYLimitesEstacionCanal(models.Model):
    estaciones = models.OneToOneField(Estaciones, models.DO_NOTHING, db_column='ESTACIONES_ID', primary_key=True)  # Field name made lowercase.
    canales = models.ForeignKey(Canales, models.DO_NOTHING, db_column='CANALES_ID')  # Field name made lowercase.
    tipo = models.IntegerField(db_column='TIPO')  # Field name made lowercase.
    valor = models.FloatField(db_column='VALOR', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'medias_y_limites_estacion_canal'
        unique_together = (('estaciones', 'canales', 'tipo'),)


class MedidasEstacionMovil(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_estacion = models.ForeignKey(Estaciones, models.DO_NOTHING, db_column='ID_ESTACION')  # Field name made lowercase.
    detector = models.CharField(db_column='DETECTOR', max_length=30)  # Field name made lowercase.
    fecha_medida = models.DateTimeField(db_column='FECHA_MEDIDA', blank=True, null=True)  # Field name made lowercase.
    tiempo_real = models.IntegerField(db_column='TIEMPO_REAL', blank=True, null=True)  # Field name made lowercase.
    tiempo_life = models.IntegerField(db_column='TIEMPO_LIFE', blank=True, null=True)  # Field name made lowercase.
    cuentas_totales = models.IntegerField(db_column='CUENTAS_TOTALES', blank=True, null=True)  # Field name made lowercase.
    cuentas = models.CharField(db_column='CUENTAS', max_length=9999, blank=True, null=True)  # Field name made lowercase.
    dosis = models.FloatField(db_column='DOSIS', blank=True, null=True)  # Field name made lowercase.
    lat = models.FloatField(db_column='LAT', blank=True, null=True)  # Field name made lowercase.
    lon = models.FloatField(db_column='LON', blank=True, null=True)  # Field name made lowercase.
    distancia = models.IntegerField(db_column='DISTANCIA', blank=True, null=True)  # Field name made lowercase.
    altura = models.IntegerField(db_column='ALTURA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'medidas_estacion_movil'


class Menmovil(models.Model):
    id_mensaje = models.AutoField(db_column='ID_MENSAJE', primary_key=True)  # Field name made lowercase.
    usuario = models.CharField(db_column='USUARIO', max_length=50)  # Field name made lowercase.
    telefono = models.CharField(db_column='TELEFONO', max_length=50)  # Field name made lowercase.
    mensaje = models.CharField(db_column='MENSAJE', max_length=160)  # Field name made lowercase.
    tipo = models.CharField(db_column='TIPO', max_length=2)  # Field name made lowercase.
    procesado = models.IntegerField(db_column='PROCESADO')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'menmovil'


class Mensaje(models.Model):
    fecha_hora = models.DateTimeField(db_column='FECHA_HORA', primary_key=True)  # Field name made lowercase.
    enviado = models.IntegerField(db_column='ENVIADO')  # Field name made lowercase.
    tipo = models.CharField(db_column='TIPO', max_length=2)  # Field name made lowercase.
    mensaje = models.CharField(db_column='MENSAJE', max_length=160)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mensaje'
        unique_together = (('fecha_hora', 'enviado', 'mensaje'),)


class MensajeHistoenvio(models.Model):
    fecha = models.DateField(db_column='FECHA', primary_key=True)  # Field name made lowercase.
    tipo = models.IntegerField(db_column='TIPO')  # Field name made lowercase.
    hora_envio = models.TimeField(db_column='HORA_ENVIO')  # Field name made lowercase.
    hora_confirmacion = models.TimeField(db_column='HORA_CONFIRMACION')  # Field name made lowercase.
    usuario = models.CharField(db_column='USUARIO', max_length=30)  # Field name made lowercase.
    remite = models.CharField(db_column='REMITE', max_length=30)  # Field name made lowercase.
    movil = models.CharField(db_column='MOVIL', max_length=12)  # Field name made lowercase.
    mensaje = models.CharField(db_column='MENSAJE', max_length=160)  # Field name made lowercase.
    intentos = models.IntegerField(db_column='INTENTOS')  # Field name made lowercase.
    confirmado = models.IntegerField(db_column='CONFIRMADO')  # Field name made lowercase.
    enviado = models.CharField(db_column='ENVIADO', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mensaje_histoenvio'
        unique_together = (('fecha', 'tipo', 'hora_envio', 'hora_confirmacion', 'movil'),)


class MensajesAlertas(models.Model):
    id_alertas = models.AutoField(db_column='ID_ALERTAS', primary_key=True)  # Field name made lowercase.
    f_h_inicial = models.DateTimeField(db_column='F_H_INICIAL')  # Field name made lowercase.
    estaciones = models.ForeignKey(Estaciones, models.DO_NOTHING, db_column='ESTACIONES_ID')  # Field name made lowercase.
    canales_id = models.IntegerField(db_column='CANALES_ID')  # Field name made lowercase.
    mensaje = models.TextField(db_column='MENSAJE')  # Field name made lowercase.
    tipo = models.IntegerField(db_column='TIPO')  # Field name made lowercase.
    enviado = models.IntegerField(db_column='ENVIADO', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mensajes_alertas'
        unique_together = (('id_alertas', 'f_h_inicial', 'estaciones', 'canales_id'),)


class MensajesAnalista(models.Model):
    id_mensaje_analista = models.IntegerField(db_column='ID_MENSAJE_ANALISTA', primary_key=True)  # Field name made lowercase.
    descripcion = models.TextField(db_column='DESCRIPCION')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mensajes_analista'


class MensajesAyudaDecision(models.Model):
    id_ayuda = models.IntegerField(db_column='ID_AYUDA', primary_key=True)  # Field name made lowercase.
    id_mensaje_alerta = models.IntegerField(db_column='ID_MENSAJE_ALERTA')  # Field name made lowercase.
    mensaje_ayuda = models.TextField(db_column='MENSAJE_AYUDA')  # Field name made lowercase.
    tipo = models.IntegerField(db_column='TIPO', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mensajes_ayuda_decision'
        unique_together = (('id_ayuda', 'id_mensaje_alerta'),)


class MensajesPredefinidos(models.Model):
    id_mensaje = models.IntegerField(db_column='ID_MENSAJE', primary_key=True)  # Field name made lowercase.
    descripcion_corta = models.CharField(db_column='DESCRIPCION_CORTA', max_length=250, blank=True, null=True)  # Field name made lowercase.
    descripcion_larga = models.TextField(db_column='DESCRIPCION_LARGA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mensajes_predefinidos'


class Meteo(models.Model):
    id = models.BigAutoField(primary_key=True)
    idgeopos = models.ForeignKey(Geopos, models.DO_NOTHING, db_column='idgeopos', blank=True, null=True)
    direccion_viento = models.FloatField(blank=True, null=True)
    velocidad_viento = models.FloatField(blank=True, null=True)
    temperatura = models.FloatField(blank=True, null=True)
    presion = models.FloatField(blank=True, null=True)
    humedad = models.FloatField(blank=True, null=True)
    lluvia = models.FloatField(blank=True, null=True)
    granizo = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'meteo'


class Monitoriza(models.Model):
    fecha_hora = models.DateTimeField(db_column='FECHA_HORA', primary_key=True)  # Field name made lowercase.
    id_estacion = models.IntegerField(db_column='ID_ESTACION')  # Field name made lowercase.
    id_canal = models.IntegerField(db_column='ID_CANAL')  # Field name made lowercase.
    mensaje = models.CharField(db_column='MENSAJE', max_length=20)  # Field name made lowercase.
    leido = models.IntegerField(db_column='LEIDO')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'monitoriza'
        unique_together = (('fecha_hora', 'id_estacion', 'id_canal'),)


class Niveles(models.Model):
    fecha_hora = models.DateTimeField(db_column='FECHA_HORA', primary_key=True)  # Field name made lowercase.
    estacion = models.IntegerField(db_column='ESTACION')  # Field name made lowercase.
    canal = models.IntegerField(db_column='CANAL')  # Field name made lowercase.
    detector = models.IntegerField(db_column='DETECTOR')  # Field name made lowercase.
    isotopo = models.IntegerField(db_column='ISOTOPO')  # Field name made lowercase.
    nivel = models.IntegerField(db_column='NIVEL')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'niveles'
        unique_together = (('fecha_hora', 'estacion', 'canal', 'detector', 'isotopo', 'nivel'),)


class ParamControl(models.Model):
    fecha_hora = models.DateTimeField(db_column='FECHA_HORA', primary_key=True)  # Field name made lowercase.
    estaciones = models.ForeignKey(Estaciones, models.DO_NOTHING, db_column='ESTACIONES_ID')  # Field name made lowercase.
    canales = models.ForeignKey(Canales, models.DO_NOTHING, db_column='CANALES_ID')  # Field name made lowercase.
    valor = models.FloatField(db_column='VALOR', blank=True, null=True)  # Field name made lowercase.
    valido = models.IntegerField(db_column='VALIDO', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'param_control'
        unique_together = (('fecha_hora', 'estaciones', 'canales'),)


class PosicionamientoMedida(models.Model):
    fecha_hora = models.DateTimeField(db_column='FECHA_HORA', primary_key=True)  # Field name made lowercase.
    estaciones_id = models.IntegerField(db_column='ESTACIONES_ID')  # Field name made lowercase.
    latitud = models.FloatField(db_column='LATITUD', blank=True, null=True)  # Field name made lowercase.
    longitud = models.FloatField(db_column='LONGITUD', blank=True, null=True)  # Field name made lowercase.
    valor = models.FloatField(db_column='VALOR', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'posicionamiento_medida'
        unique_together = (('fecha_hora', 'estaciones_id'),)


class PosicionesProyectosMedida(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    n_pos = models.IntegerField(db_column='N_POS', blank=True, null=True)  # Field name made lowercase.
    proyecto = models.CharField(db_column='PROYECTO', max_length=60)  # Field name made lowercase.
    lat = models.CharField(db_column='LAT', max_length=60)  # Field name made lowercase.
    lon = models.CharField(db_column='LON', max_length=60)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'posiciones_proyectos_medida'


class RadwinRvra(models.Model):
    ruta = models.CharField(db_column='RUTA', max_length=10, blank=True, null=True)  # Field name made lowercase.
    radwin = models.CharField(db_column='RADWIN', max_length=50, blank=True, null=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='CODIGO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    d_ip = models.CharField(db_column='D_IP', primary_key=True, max_length=15)  # Field name made lowercase.
    fecha_hora = models.DateTimeField(db_column='FECHA_HORA', blank=True, null=True)  # Field name made lowercase.
    estado = models.IntegerField(db_column='ESTADO', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'radwin_rvra'


class Relacion(models.Model):
    estac = models.IntegerField(db_column='ESTAC', primary_key=True)  # Field name made lowercase.
    canal = models.IntegerField(db_column='CANAL')  # Field name made lowercase.
    monitorizar = models.FloatField(db_column='MONITORIZAR')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'relacion'
        unique_together = (('estac', 'canal'),)


class RelacionConexionesEstaciones(models.Model):
    id_estacion = models.OneToOneField(Estaciones, models.DO_NOTHING, db_column='ID_ESTACION', primary_key=True)  # Field name made lowercase.
    id_conexion = models.ForeignKey('TipoConexion', models.DO_NOTHING, db_column='ID_CONEXION')  # Field name made lowercase.
    limite_tiempo = models.IntegerField(db_column='LIMITE_TIEMPO', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'relacion_conexiones_estaciones'
        unique_together = (('id_estacion', 'id_conexion'),)


class RelacionDetectoresEstacion(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_estacion = models.IntegerField(db_column='ID_ESTACION')  # Field name made lowercase.
    id_detector = models.IntegerField(db_column='ID_DETECTOR')  # Field name made lowercase.
    dir_datos = models.CharField(db_column='DIR_DATOS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ref_id = models.CharField(db_column='REF_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'relacion_detectores_estacion'


class RelacionDetectoresIsotopos(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    rel_det_est = models.ForeignKey(RelacionDetectoresEstacion, models.DO_NOTHING, db_column='REL_DET_EST_ID')  # Field name made lowercase.
    isototo = models.ForeignKey(Isotopos, models.DO_NOTHING, db_column='ISOTOTO_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'relacion_detectores_isotopos'


class RelacionInformesDatosCorregidos(models.Model):
    id_informes = models.IntegerField(primary_key=True)
    id_datos_corregidos = models.IntegerField()
    id_mensaje = models.IntegerField()
    tipo_mensaje = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'relacion_informes_datos_corregidos'
        unique_together = (('id_informes', 'id_datos_corregidos'),)


class RelacionPosicionesMedidas(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_punto = models.IntegerField(db_column='ID_PUNTO')  # Field name made lowercase.
    analista = models.CharField(db_column='ANALISTA', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fecha_hora = models.DateTimeField(db_column='FECHA_HORA', blank=True, null=True)  # Field name made lowercase.
    dosis = models.CharField(db_column='DOSIS', max_length=60, blank=True, null=True)  # Field name made lowercase.
    cuentas = models.IntegerField(db_column='CUENTAS', blank=True, null=True)  # Field name made lowercase.
    tiempo_medida = models.IntegerField(db_column='TIEMPO_MEDIDA', blank=True, null=True)  # Field name made lowercase.
    unidad_tiempo = models.CharField(db_column='UNIDAD_TIEMPO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    comentario = models.CharField(db_column='COMENTARIO', max_length=300, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'relacion_posiciones_medidas'


class RelacionRoles(models.Model):
    rol_id = models.IntegerField(db_column='ROL_ID', primary_key=True)  # Field name made lowercase.
    tipo_rol = models.CharField(db_column='TIPO_ROL', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'relacion_roles'


class RelacionVbResponsableCanal(models.Model):
    id_canal = models.IntegerField(primary_key=True)
    id_usuario_responsable = models.IntegerField()
    orden = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'relacion_vb_responsable_canal'
        unique_together = (('id_canal', 'id_usuario_responsable'),)


class RevisionGraficas(models.Model):
    usuario = models.CharField(max_length=90)
    fecha = models.DateTimeField()
    comentarios = models.CharField(max_length=40000)
    operatividad = models.CharField(max_length=300)
    niveles = models.CharField(max_length=300)
    integridad = models.CharField(max_length=300)
    grafica = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'revision_graficas'


class Sesion(models.Model):
    fecha = models.DateTimeField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    activa = models.IntegerField(blank=True, null=True)
    id_dispositivo = models.ForeignKey(DispositivosMoviles, models.DO_NOTHING, db_column='id_dispositivo', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sesion'


class SesionesMoviles(models.Model):
    id = models.IntegerField(primary_key=True)
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    nombre_sesion = models.CharField(max_length=30, blank=True, null=True)
    descripcion = models.CharField(max_length=300, blank=True, null=True)
    id_disp_movil = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sesiones_moviles'


class SimulacrosRarex(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    fecha = models.CharField(db_column='FECHA', max_length=300)  # Field name made lowercase.
    estado = models.IntegerField(db_column='ESTADO', blank=True, null=True)  # Field name made lowercase.
    inicio_nivel1 = models.DateTimeField(db_column='INICIO_NIVEL1', blank=True, null=True)  # Field name made lowercase.
    minutos_nivel1 = models.IntegerField(db_column='MINUTOS_NIVEL1', blank=True, null=True)  # Field name made lowercase.
    inicio_nivel2 = models.DateTimeField(db_column='INICIO_NIVEL2', blank=True, null=True)  # Field name made lowercase.
    minutos_nivel2 = models.IntegerField(db_column='MINUTOS_NIVEL2', blank=True, null=True)  # Field name made lowercase.
    inicio_nivel3 = models.DateTimeField(db_column='INICIO_NIVEL3', blank=True, null=True)  # Field name made lowercase.
    minutos_nivel3 = models.IntegerField(db_column='MINUTOS_NIVEL3', blank=True, null=True)  # Field name made lowercase.
    exitoso = models.IntegerField(db_column='EXITOSO', blank=True, null=True)  # Field name made lowercase.
    analista_guardia = models.IntegerField(db_column='ANALISTA_GUARDIA', blank=True, null=True)  # Field name made lowercase.
    analista_confirmacion = models.IntegerField(db_column='ANALISTA_CONFIRMACION', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'simulacros_rarex'


class TablaStatusUsuarios(models.Model):
    id_usuario = models.IntegerField(db_column='ID_USUARIO', primary_key=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='STATUS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tabla_status_usuarios'


class TipoConexion(models.Model):
    id_conex = models.IntegerField(db_column='ID_CONEX', primary_key=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='TIPO', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tipo_conexion'


class TipoMensaje(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    tipo_mensaje = models.CharField(db_column='TIPO_MENSAJE', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tipo_mensaje'


class UbicacionesInteres(models.Model):
    id_ubicacion = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=120, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    tipo = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ubicaciones_interes'


class UltimosValoresRecibidos(models.Model):
    fecha_hora = models.DateTimeField(db_column='FECHA_HORA')  # Field name made lowercase.
    estacion_id = models.IntegerField(db_column='ESTACION_ID', primary_key=True)  # Field name made lowercase.
    can_det_est = models.IntegerField(db_column='CAN_DET_EST')  # Field name made lowercase.
    isotopo_id = models.IntegerField(db_column='ISOTOPO_ID')  # Field name made lowercase.
    valor = models.FloatField(db_column='VALOR', blank=True, null=True)  # Field name made lowercase.
    color = models.IntegerField(db_column='COLOR', blank=True, null=True)  # Field name made lowercase.
    error = models.FloatField(db_column='ERROR', blank=True, null=True)  # Field name made lowercase.
    amd = models.FloatField(db_column='AMD', blank=True, null=True)  # Field name made lowercase.
    unidades = models.CharField(db_column='UNIDADES', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ultimos_valores_recibidos'
        unique_together = (('estacion_id', 'can_det_est', 'isotopo_id'),)


class UsuariosMenmovil(models.Model):
    codigo = models.CharField(db_column='CODIGO', primary_key=True, max_length=2)  # Field name made lowercase.
    usuario = models.CharField(db_column='USUARIO', max_length=100)  # Field name made lowercase.
    tipo = models.CharField(db_column='TIPO', max_length=1)  # Field name made lowercase.
    spida = models.IntegerField(db_column='SPIDA')  # Field name made lowercase.
    telefono = models.CharField(db_column='TELEFONO', max_length=12)  # Field name made lowercase.
    guardia = models.IntegerField(db_column='GUARDIA')  # Field name made lowercase.
    finde = models.IntegerField(db_column='FINDE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'usuarios_menmovil'
        unique_together = (('codigo', 'usuario'),)


class UsuariosRvra(models.Model):
    usuario_id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=80, blank=True, null=True)
    apellidos = models.CharField(max_length=250, blank=True, null=True)
    dni = models.CharField(max_length=10, blank=True, null=True)
    clave = models.CharField(max_length=50)
    nivel = models.IntegerField()
    tfno_1 = models.CharField(max_length=20, blank=True, null=True)
    tfno_2 = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios_rvra'
