from django.db import models
# from dbview import DbView

# Create your models here.
class Synesisit(models.Model):
    meter_no = models.IntegerField(db_column='Meter_no')  # Field name made lowercase.
    connected_load = models.IntegerField(db_column='Connected_load')  # Field name made lowercase.
    date = models.DateField(db_column='Date')  # Field name made lowercase.
    time = models.TimeField(db_column='Time')  # Field name made lowercase.
    phase_1_line_to_neutral_volts = models.CharField(max_length=50)
    phase_1_current = models.CharField(max_length=50)
    phase_1_power = models.CharField(max_length=50)
    phase_1_volt_amps = models.CharField(max_length=50)
    phase_1_volt_amps_reactive = models.CharField(max_length=50)
    phase_1_power_factor = models.CharField(max_length=50)
    phase_2_line_to_neutral_volts = models.CharField(max_length=50)
    phase_2_current = models.CharField(max_length=50)
    phase_2_power = models.CharField(max_length=50)
    phase_2_volt_amps = models.CharField(max_length=50)
    phase_2_volt_amps_reactive = models.CharField(max_length=50)
    phase_2_power_factor = models.CharField(max_length=50)
    phase_3_line_to_neutral_volts = models.CharField(max_length=50)
    phase_3_current = models.CharField(max_length=50)
    phase_3_power = models.CharField(max_length=50)
    phase_3_volt_amps = models.CharField(max_length=50)
    phase_3_volt_amps_reactive = models.CharField(max_length=50)
    phase_3_power_factor = models.CharField(max_length=50)
    average_line_to_neutral_volts = models.CharField(max_length=50)
    average_line_current = models.CharField(max_length=50)
    sum_of_line_currents = models.CharField(max_length=50)
    total_system_power = models.CharField(max_length=50)
    total_system_volt_amps = models.CharField(max_length=50)
    total_system_var = models.CharField(max_length=50)
    total_system_power_factor = models.CharField(max_length=50)
    total_system_phase_angle = models.CharField(max_length=50)
    frequency_of_supply_voltages = models.CharField(max_length=50)
    import_wh_since_last_reset = models.CharField(max_length=50)
    export_wh_since_last_reset = models.CharField(max_length=50)
    import_varh_since_last_reset = models.CharField(max_length=50)
    export_varh_since_last_reset = models.CharField(max_length=50)
    line_1_to_line_2_volts = models.CharField(max_length=50)
    line_2_to_line_3_volts = models.CharField(max_length=50)
    line_3_to_line_1_volts = models.CharField(max_length=50)
    average_line_to_line_volts = models.CharField(max_length=50)
    neutral_current = models.CharField(max_length=50)
    total_kwh = models.CharField(max_length=50)
    total_kvarh = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'SynesisIT'


class ARSynesisitDB1(models.Model):
    # sid = models.CharField(max_length=191, db_column='id')
    Meter_Number = models.CharField(max_length=5, db_column='Meter_Number')
    Phase = models.CharField(max_length=6, db_column='Phase')
    reading_dt = models.DateField(db_column='reading_dt')  # Field name made lowercase.
    prev_day = models.DateField(db_column='prev_day')
    YR = models.IntegerField(db_column='YR')
    MTH = models.IntegerField(db_column='MTH')
    WK = models.IntegerField(db_column='WK')
    Weekday = models.CharField(max_length=9, db_column='Weekday')
    cur_reading_time = models.CharField(max_length=9, db_column='cur_reading_time')
    DT = models.IntegerField(db_column='DT')
    HR = models.IntegerField(db_column='HR')
    MIN = models.IntegerField(db_column='MIN')
    Line_Current = models.CharField(max_length=50, db_column='Line_Current')
    Power = models.CharField(max_length=50, db_column='Power')
    Power_Factor = models.CharField(max_length=50, db_column='Power_Factor')
    KWH = models.CharField(max_length=50, db_column='KWH')

    class Meta:
        managed = False
        db_table = 'AR_SynesisIT_DB1'

class ARPwrPfCharts(models.Model):
    Meter_Number = models.CharField(max_length=5, db_column='Meter_Number')
    # sid = models.CharField(max_length=191, db_column='id')
    latest_reading_time = models.CharField(max_length=21, db_column='latest_reading_time')
    reading_dt = models.DateField(db_column='reading_dt')
    prev_day = models.DateField(db_column='prev_day')
    YR = models.IntegerField(db_column='YR')
    MTH = models.IntegerField(db_column='MTH')
    WK = models.IntegerField(db_column='WK')
    Weekday = models.CharField(max_length=9, db_column='Weekday')
    DT = models.IntegerField(db_column='DT')
    HR = models.IntegerField(db_column='HR')
    MIN = models.IntegerField(db_column='MIN')
    PHASE1_PWR = models.CharField(max_length=50, db_column='PHASE1_PWR')
    PHASE1_PF = models.CharField(max_length=50, db_column='PHASE1_PF')
    PHASE2_PWR = models.CharField(max_length=50, db_column='PHASE2_PWR')
    PHASE2_PF = models.CharField(max_length=50, db_column='PHASE2_PF')
    PHASE3_PWR = models.CharField(max_length=50, db_column='PHASE3_PWR')
    PHASE3_PF = models.CharField(max_length=50, db_column='PHASE3_PF')
    TOTAL_PWR = models.CharField(max_length=50, db_column='TOTAL_PWR')
    TOTAL_PF = models.CharField(max_length=50, db_column='TOTAL_PF')
    PHASE1_PWR_PREV = models.CharField(max_length=50, db_column='PHASE1_PWR_PREV')
    PHASE1_PF_PREV = models.CharField(max_length=50, db_column='PHASE1_PF_PREV')
    PHASE2_PWR_PREV = models.CharField(max_length=50, db_column='PHASE2_PWR_PREV')
    PHASE2_PF_PREV = models.CharField(max_length=50, db_column='PHASE2_PF_PREV')
    PHASE3_PWR_PREV = models.CharField(max_length=50, db_column='PHASE3_PWR_PREV')
    PHASE3_PF_PREV = models.CharField(max_length=50, db_column='PHASE3_PF_PREV')
    TOTAL_PWR_PREV = models.CharField(max_length=50, db_column='TOTAL_PWR_PREV')
    TOTAL_PF_PREV = models.CharField(max_length=50, db_column='TOTAL_PF_PREV')
    class Meta:
        managed = False
        db_table = 'AR_PWR_PF_Charts'