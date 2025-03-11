from django.db import models

# Create your models here.
class Maquina(models.Model):
    ESTAT_CHOICES = [
        ('Activa', 'Activa'),
        ('Inactiva', 'Inactiva'),
        ('Manteniment', 'Manteniment'),
    ]

    nom = models.CharField(max_length=100)  # Nom de la màquina
    model = models.CharField(max_length=50, blank=True, null=True)  # Model opcional
    fabricant = models.CharField(max_length=100, blank=True, null=True)  # Fabricant opcional
    any_fabricacio = models.PositiveSmallIntegerField(blank=True, null=True)  # Any de fabricació
    estat = models.CharField(max_length=15, choices=ESTAT_CHOICES, default='Activa')  # Estat de la màquina
    ubicacio = models.CharField(max_length=255, blank=True, null=True)  # Ubicació opcional
    data_alta = models.DateTimeField(auto_now_add=True)  # Data de registre automàtica
    ultima_revisio = models.DateField(blank=True, null=True)  # Última revisió opcional
    descripcio = models.TextField(blank=True, null=True)  # Descripció opcional

    def __str__(self):
        return f"{self.nom} ({self.model})"
    
class Sensor(models.Model):
    TIPUS_CHOICES = [
        ('Temperatura', 'Temperatura'),
        ('Vibració', 'Vibració'),
        ('Pressió', 'Pressió'),
        ('Consum Elèctric', 'Consum Elèctric'),
        ('Altres', 'Altres'),
    ]

    ESTAT_CHOICES = [
        ('Actiu', 'Actiu'),
        ('Inactiu', 'Inactiu'),
        ('Manteniment', 'Manteniment'),
    ]
    
    maquina = models.ForeignKey('Maquina', on_delete=models.CASCADE, related_name='sensors')  # Relació amb Maquina
    tipus = models.CharField(max_length=20, choices=TIPUS_CHOICES)  # Tipus de sensor
    unitat = models.CharField(max_length=20, blank=True, null=True)  # Unitat opcional
    fabricant = models.CharField(max_length=100, blank=True, null=True)  # Fabricant opcional
    model = models.CharField(max_length=50, blank=True, null=True)  # Model opcional
    data_instalacio = models.DateTimeField(auto_now_add=True)  # Data d'instal·lació automàtica
    estat = models.CharField(max_length=15, choices=ESTAT_CHOICES, default='Actiu')  # Estat del sensor
    descripcio = models.TextField(blank=True, null=True)  # Descripció opcional

    def __str__(self):
        return f"{self.tipus} ({self.model}) - {self.maquina.nom}"

class ConfiguracioSensor(models.Model):
    sensor = models.ForeignKey('Sensor', on_delete=models.CASCADE, related_name='configuracions')  # Relació amb Sensor
    tipus = models.CharField(max_length=50)  # Exemple: "Temperatura Màxima"
    valor_max = models.DecimalField(max_digits=10, decimal_places=2)  # Valor màxim requerit
    valor_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Opcional
    unitat = models.CharField(max_length=20, blank=True, null=True)  # Unitat opcional

    def __str__(self):
        return f"{self.tipus} ({self.valor_min} - {self.valor_max} {self.unitat}) - {self.sensor.tipus}"

class TransaccioSensor(models.Model):
    sensor = models.ForeignKey('Sensor', on_delete=models.CASCADE, related_name='transaccions')  # Relació amb Sensor
    valor = models.DecimalField(max_digits=10, decimal_places=2)  # Valor mesurat pel sensor
    unitat = models.CharField(max_length=20)  # Unitat de mesura (°C, Hz, bar, kW, etc.)
    timestamp_registre = models.DateTimeField(auto_now_add=True)  # Data i hora automàtica de la lectura

    def __str__(self):
        return f"{self.sensor.tipus} - {self.valor} {self.unitat} ({self.timestamp_registre})"
class LogAccio(models.Model):
    usuari = models.ForeignKey('Usuari', on_delete=models.SET_NULL, null=True, related_name='logs')  # Relació amb l'usuari
    accio = models.CharField(max_length=255)  # Descripció de l'acció realitzada
    timestamp_accio = models.DateTimeField(auto_now_add=True)  # Quan es va registrar l'acció

    def __str__(self):
        return f"{self.usuari} - {self.accio} ({self.timestamp_accio})"
    

class AlertaSensor(models.Model):
    TIPUS_ALERTA_CHOICES = [
        ('Alta Temperatura', 'Alta Temperatura'),
        ('Baixa Pressió', 'Baixa Pressió'),
        ('Vibració Excessiva', 'Vibració Excessiva'),
        ('Sobreconsum Elèctric', 'Sobreconsum Elèctric'),
    ]

    ESTAT_ALERTA_CHOICES = [
        ('Nou', 'Nou'),
        ('Revisat', 'Revisat'),
        ('Ignorat', 'Ignorat'),
    ]

    sensor = models.ForeignKey('Sensor', on_delete=models.CASCADE, related_name='alertes')  # Relació amb el sensor
    tipus_alerta = models.CharField(max_length=50, choices=TIPUS_ALERTA_CHOICES)  # Tipus de l'alerta
    valor_detectat = models.DecimalField(max_digits=10, decimal_places=2)  # Valor detectat pel sensor
    unitat = models.CharField(max_length=20, blank=True, null=True)  # Unitat de mesura
    timestamp_alerta = models.DateTimeField(auto_now_add=True)  # Quan es va generar l'alerta
    estat = models.CharField(max_length=15, choices=ESTAT_ALERTA_CHOICES, default='Nou')  # Estat de l'alerta

    def __str__(self):
        return f"Alerta: {self.tipus_alerta} - {self.valor_detectat} {self.unitat} ({self.timestamp_alerta})"
