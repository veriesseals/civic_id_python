from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(
                blank=True,
                choices=[
                    ('SUPER_ADMIN',     'Super Admin'),
                    ('REGISTRAR',       'Registrar'),
                    ('DMV',             'DMV'),
                    ('LAW_ENFORCEMENT', 'Law Enforcement'),
                    ('AUDITOR',         'Auditor'),
                    ('ELECTIONS',       'Elections'),
                    ('STATE_DEPT',      'State Department'),
                    ('SSA',             'Social Security Administration'),
                    ('IMMIGRATION',     'Immigration Services'),
                ],
                max_length=50,
                null=True,
            ),
        ),
    ]