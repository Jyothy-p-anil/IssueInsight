
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0012_incident"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name="IncidentTicket",
                    fields=[
                        (
                            "id",
                            models.BigAutoField(
                                auto_created=True,
                                primary_key=True,
                                serialize=False,
                                verbose_name="ID",
                            ),
                        ),
                        (
                            "incident",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                to="tickets.incident",
                            ),
                        ),
                        (
                            "ticket",
                            models.OneToOneField(
                                on_delete=django.db.models.deletion.CASCADE,
                                to="tickets.ticket",
                            ),
                        ),
                    ],
                    options={
                        "db_table": "tickets_incident_tickets",
                    },
                ),
                migrations.AlterField(
                    model_name="incident",
                    name="tickets",
                    field=models.ManyToManyField(
                        blank=True,
                        related_name="incidents",
                        through="tickets.IncidentTicket",
                        to="tickets.ticket",
                    ),
                ),
                migrations.AddConstraint(
                    model_name="incidentticket",
                    constraint=models.UniqueConstraint(
                        fields=("incident", "ticket"),
                        name="unique_incident_ticket_link",
                    ),
                ),
            ],
            database_operations=[
                migrations.RunSQL(
                    sql=(
                        "CREATE UNIQUE INDEX "
                        "unique_incident_ticket_id "
                        "ON tickets_incident_tickets (ticket_id)"
                    ),
                    reverse_sql=(
                        "DROP INDEX IF EXISTS "
                        "unique_incident_ticket_id"
                    ),
                ),
            ],
        ),
    ]
