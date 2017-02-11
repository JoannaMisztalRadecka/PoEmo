from __future__ import unicode_literals
import json
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible  # only if you need to support Python 2
class Inspiration(models.Model):
    input_text = models.TextField(max_length=1000)
    template = models.CharField(max_length=20, default="[8,8,8,8,0,8,8,8,8]")

    def settemplate(self, x):
        self.foo = json.dumps(x)

    def gettemplate(self):
        return json.loads(self.foo)

    def __str__(self):
        return self.input_text

@python_2_unicode_compatible  # only if you need to support Python 2
class Poem(models.Model):
    poem_text = models.TextField(max_length=10000)
    inspiration = models.ForeignKey(Inspiration, on_delete=models.CASCADE)

    def __str__(self):
        return self.poem_text