from django.db import models
import uuid

class Employee(models.Model):
    empid = models.CharField(max_length=8, primary_key=True)
    empfname = models.CharField(max_length=64)
    emplname = models.CharField(max_length=64)
    emppasswd = models.CharField(max_length=256)
    emprole = models.IntegerField()


class Shiiregyosha(models.Model):
    shiireid = models.CharField(max_length=8, primary_key=True, verbose_name='仕入れ先ID')
    shiiremei = models.CharField(max_length=64, verbose_name='仕入れ先名')
    shiireaddress = models.CharField(max_length=64, verbose_name='仕入れ先住所')
    shiiretel = models.CharField(max_length=13, verbose_name='仕入れ先電話番号')
    shihonkin = models.IntegerField(verbose_name='資本金')
    nouki = models.IntegerField(verbose_name='納期')

class Tabyouin(models.Model):
    tabyouinid = models.CharField('他病院ID', max_length=8, primary_key=True)
    tabyouinmei = models.CharField('他病院名', max_length=64)
    tabyouinaddress = models.CharField('他病院住所', max_length=64)
    tabyouintel = models.CharField('他病院電話番号', max_length=13)
    tabyouinshihonkin = models.IntegerField('資本金')
    kyukyu = models.IntegerField('救急フラグ')




class Patient(models.Model):
    patid = models.CharField(max_length=8, primary_key=True, verbose_name='患者ID')
    patfname = models.CharField(max_length=64, verbose_name='患者名')
    patlname = models.CharField(max_length=64, verbose_name='患者姓')
    hokenmei = models.CharField(max_length=64, verbose_name='保険証記号番号')
    hokenexp = models.DateField(verbose_name='有効期限')


class Medicine(models.Model):
    medicineid = models.CharField('薬剤ID', max_length=8, primary_key=True)
    medicinename = models.CharField('薬剤名', max_length=64)
    unit = models.CharField('単位', max_length=8)

class Treatment(models.Model):
    treatmentid = models.CharField(max_length=8, primary_key=True, default=uuid.uuid4)
    quantity = models.IntegerField()
    treatmentdata = models.TextField()
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

