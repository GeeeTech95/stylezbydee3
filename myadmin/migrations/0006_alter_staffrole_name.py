# Generated by Django 4.2.15 on 2024-09-28 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0005_department_staffrole_remove_staff_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffrole',
            name='name',
            field=models.CharField(choices=[('ceo', 'Ceo'), ('general manager', 'General manager'), ('recruitment manager', 'Recruitment manager'), ('safety manager', 'Safety manager'), ('design', 'Design'), ('social media manager', 'Social media manager'), ('customer service', 'Customer service'), ('technical manager', 'Technical manager'), ('maintenance manager', 'Maintenance manager'), ('quality control manager', 'Quality control manager'), ('sales repesentative', 'Sales repesentative'), ('personal assistant to ceo', 'Personal assistant to ceo'), ('head tailor', 'Head tailor'), ('head beeder', 'Head beeder'), ('head stoner', 'Head stoner'), ('no role', 'No role')], max_length=50),
        ),
    ]
