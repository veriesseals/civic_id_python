import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('persons', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VoterRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_number', models.CharField(max_length=100, unique=True)),
                ('party_affiliation', models.CharField(
                    choices=[
                        ('DEMOCRATIC','Democratic'),('REPUBLICAN','Republican'),
                        ('INDEPENDENT','Independent'),('GREEN','Green'),
                        ('LIBERTARIAN','Libertarian'),('OTHER','Other'),
                        ('UNAFFILIATED','Unaffiliated'),
                    ],
                    default='UNAFFILIATED', max_length=50
                )),
                ('precinct', models.CharField(blank=True, max_length=100, null=True)),
                ('county', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('registration_date', models.DateField()),
                ('status', models.CharField(
                    choices=[
                        ('ACTIVE','Active'),('INACTIVE','Inactive'),
                        ('SUSPENDED','Suspended'),('INELIGIBLE','Ineligible'),
                        ('RESTORED','Restored'),
                    ],
                    default='ACTIVE', max_length=20
                )),
                ('ineligibility_reason', models.CharField(
                    blank=True,
                    choices=[
                        ('FELONY','Felony Conviction'),('AGE','Under 18'),
                        ('NON_CITIZEN','Non-Citizen'),('OTHER','Other'),
                    ],
                    max_length=20, null=True
                )),
                ('has_felony_record', models.BooleanField(default=False)),
                ('felony_resolved', models.BooleanField(default=False)),
                ('restored_at', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('person', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='voter_registration',
                    to='persons.person'
                )),
                ('restored_by', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='restorations_processed',
                    to=settings.AUTH_USER_MODEL
                )),
            ],
        ),
        migrations.CreateModel(
            name='VoterID',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voter_id_number', models.CharField(max_length=100, unique=True)),
                ('issue_date', models.DateField()),
                ('expiration_date', models.DateField()),
                ('status', models.CharField(
                    choices=[
                        ('ACTIVE','Active'),('EXPIRED','Expired'),
                        ('REVOKED','Revoked'),('SUSPENDED','Suspended'),
                    ],
                    default='ACTIVE', max_length=20
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('person', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='voter_ids',
                    to='persons.person'
                )),
                # ← Fixed: uses 'voter_registration' app label (not 'apps_voter_registration')
                ('registration', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='voter_id',
                    to='voter_registration.voterregistration'
                )),
            ],
        ),
    ]