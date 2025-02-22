# Generated by Django 4.2.15 on 2024-12-18 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashion', '0021_alter_catalogueimage_options_catalogue_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bespokeorder',
            name='agbada_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Agbada Length'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='armhole_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Armhole Circumference'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='back_depth',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Back Depth'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='blouse_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Blouse Length'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='bottom_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Bottom Circumference'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='buba_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Buba Length'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='bust_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Bust Circumference'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='bust_point',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Bust Point'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='calf_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Calf Circumference'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='chest_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Chest Circumference'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='hip_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Hip Circumference'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='iro_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Iro Length'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='jacket_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Jacket Length'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='jacket_sleeve_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Jacket Sleeve Length'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='kaftan_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Kaftan Length'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='knee_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Knee Circumference'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='lap_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Lap Circumference'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='long_gown_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Long Gown Length'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='long_skirt_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Long Skirt Length'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='neck_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Neck Circumference'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='nipple_point_2_point_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Nipple Point-to-Point Length'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='round_sleeves_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Round Sleeves Circumference'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='round_underbust',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Underbust Circumference'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='senator_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Senator Length'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='short_gown_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Short Gown Length'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='short_skirt_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Short Skirt Length'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='shoulder_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Shoulder Length'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='shoulder_to_halflength',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Shoulder to Halflength'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='shoulder_to_hip',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Shoulder to Hip'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='shoulder_to_knee',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Shoulder to Knee'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='shoulder_to_underbust',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Shoulder to Underbust'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='skirt_waist_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Skirt Waist Circumference'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='sleeve_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Sleeve Length'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='top_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Top Length'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='trouser_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Trouser Length'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='trouser_waist_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Trouser Waist Circumference'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='waist_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Waist Circumference'),
        ),
        migrations.AlterField(
            model_name='bespokeorder',
            name='waistcoat_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Waistcoat Length'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='agbada_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Agbada Length'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='armhole_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Armhole Circumference'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='back_depth',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Back Depth'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='blouse_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Blouse Length'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='bottom_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Bottom Circumference'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='buba_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Buba Length'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='bust_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Bust Circumference'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='bust_point',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Bust Point'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='calf_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Calf Circumference'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='chest_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Chest Circumference'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='hip_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Hip Circumference'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='iro_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Iro Length'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='jacket_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Jacket Length'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='jacket_sleeve_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Jacket Sleeve Length'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='kaftan_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Kaftan Length'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='knee_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Knee Circumference'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='lap_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Lap Circumference'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='long_gown_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Long Gown Length'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='long_skirt_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Long Skirt Length'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='neck_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Neck Circumference'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='nipple_point_2_point_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Nipple Point-to-Point Length'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='round_sleeves_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Round Sleeves Circumference'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='round_underbust',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Underbust Circumference'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='senator_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Senator Length'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='short_gown_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Short Gown Length'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='short_skirt_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Short Skirt Length'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='shoulder_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Shoulder Length'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='shoulder_to_halflength',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Shoulder to Halflength'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='shoulder_to_hip',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Shoulder to Hip'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='shoulder_to_knee',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Shoulder to Knee'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='shoulder_to_underbust',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Shoulder to Underbust'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='skirt_waist_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Skirt Waist Circumference'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='sleeve_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Sleeve Length'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='top_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Top Length'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='trouser_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Trouser Length'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='trouser_waist_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Trouser Waist Circumference'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='waist_circumference',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Waist Circumference'),
        ),
        migrations.AlterField(
            model_name='clientbodymeasurement',
            name='waistcoat_length',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Waistcoat Length'),
        ),
    ]
