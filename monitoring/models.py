from django.conf import settings
from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.name


class Station(models.Model):
    name = models.CharField(max_length=120)

    code = models.CharField(
        max_length=30,
        unique=True,
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="stations",
    )

    tags = models.ManyToManyField(
        Tag,
        related_name="stations",
        blank=True,
    )

    active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.code} - {self.name}"


class StationMetadata(models.Model):
    station = models.OneToOneField(
        Station,
        on_delete=models.CASCADE,
        related_name="metadata",
    )

    elevation_m = models.FloatField(
        null=True,
        blank=True,
    )

    installation_date = models.DateField(
        null=True,
        blank=True,
    )

    operator = models.CharField(
        max_length=120,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    maintenance_note = models.TextField(
        blank=True,
    )

    def __str__(self):
        return f"Metadata for {self.station.code}"


class Sensor(models.Model):
    class SensorType(models.TextChoices):
        TEMPERATURE = "temperature", "Temperature"
        HUMIDITY = "humidity", "Humidity"
        PRESSURE = "pressure", "Pressure"
        PRECIPITATION = "precipitation", "Precipitation"

    station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="sensors",
    )

    name = models.CharField(
        max_length=100,
    )

    sensor_type = models.CharField(
        max_length=30,
        choices=SensorType.choices,
    )

    unit = models.CharField(
        max_length=20,
    )

    active = models.BooleanField(
        default=True,
    )

    installed_at = models.DateField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.station.code} - {self.name}"


class Measurement(models.Model):
    class QualityFlag(models.TextChoices):
        VALID = "valid", "Valid"
        SUSPECT = "suspect", "Suspect"
        INVALID = "invalid", "Invalid"

    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        related_name="measurements",
    )

    timestamp = models.DateTimeField()

    value = models.FloatField()

    quality_flag = models.CharField(
        max_length=20,
        choices=QualityFlag.choices,
        default=QualityFlag.VALID,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-timestamp"]

        constraints = [
            models.UniqueConstraint(
                fields=["sensor", "timestamp"],
                name="unique_measurement_per_sensor_timestamp",
            )
        ]

    def __str__(self):
        return (
            f"{self.sensor.name} - "
            f"{self.timestamp:%Y-%m-%d %H:%M} - "
            f"{self.value}"
        )
