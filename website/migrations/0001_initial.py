# Generated by Django 5.0.4 on 2024-08-15 15:53

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import website.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category_blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Category_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('farsi_name', models.CharField(default='', max_length=75)),
                ('hex_color', models.CharField(max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='Special_offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_started', models.DateTimeField(auto_now=True)),
                ('date_end', models.DateTimeField()),
                ('is_active', models.BooleanField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('phone_number', models.CharField(blank=True, max_length=20, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('eamil', models.EmailField(blank=True, max_length=254, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('last_session_key', models.CharField(blank=True, default=None, max_length=40, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', website.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='Not payed', max_length=100)),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('tracking_code', models.CharField(blank=True, max_length=255, null=True)),
                ('date_payed', models.DateField(blank=True, null=True)),
                ('time_payed', models.TimeField(blank=True, null=True)),
                ('gateway_payed', models.CharField(blank=True, max_length=150, null=True)),
                ('location', models.TextField(blank=True, null=True)),
                ('offer_present', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('description', models.TextField(blank=True, null=True)),
                ('session_key', models.CharField(blank=True, max_length=40, null=True)),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('main_image', models.ImageField(upload_to='')),
                ('content', models.TextField()),
                ('date_publish', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField(auto_now=True)),
                ('views', models.IntegerField(default=1)),
                ('author', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.category_blog')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='بدون عنوان', max_length=120)),
                ('email', models.EmailField(max_length=254)),
                ('content', models.TextField()),
                ('rating', models.IntegerField()),
                ('date_publish', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments_likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.comments')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('details', models.TextField(null=True)),
                ('date_added', models.DateField(auto_now_add=True, null=True)),
                ('main_image', models.ImageField(upload_to='')),
                ('second_image', models.ImageField(null=True, upload_to='')),
                ('rate', models.IntegerField(null=True)),
                ('price', models.IntegerField()),
                ('sell_count', models.IntegerField()),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.category_product')),
                ('colors', models.ManyToManyField(to='website.color')),
            ],
        ),
        migrations.AddField(
            model_name='comments',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.product'),
        ),
        migrations.CreateModel(
            name='Cart_item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.cart')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.color')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.product')),
            ],
        ),
        migrations.CreateModel(
            name='Product_images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.product')),
            ],
        ),
        migrations.CreateModel(
            name='Wishlists',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(blank=True, max_length=40, null=True)),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Wishlists_items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.product')),
                ('wishlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.wishlists')),
            ],
        ),
    ]
