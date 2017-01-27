from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible  # only if you need to support Python 2
class Inspiration(models.Model):
    input_text = models.TextField(max_length=1000)

    def __str__(self):
        return self.input_text

@python_2_unicode_compatible  # only if you need to support Python 2
class Poem(models.Model):
    poem_text = models.TextField(max_length=1000)
    inspiration = models.ForeignKey(Inspiration, on_delete=models.CASCADE)

    def __str__(self):
        return self.poem_text