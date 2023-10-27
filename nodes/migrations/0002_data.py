
from django.db import migrations
from nodes.models import Node

def load_data(*args):
    Node.objects.create(
        value = "ROOT",
    )

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nodes', '0001_initial')
    ]

    operations = [
        migrations.RunPython(load_data, migrations.RunPython.noop)
    ]
