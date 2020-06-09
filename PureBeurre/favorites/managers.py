"""
This file contains manager of Favorite model
"""
from django.db import models


# -tc- attention globalement à respecter la PEP 257 pour les docstrings. 
# -tc- je recommande l'utilisation de docformatter 
# -tc- (pip install docformatter, docformatter --recursive --in-place .)
class FavoriteManager(models.Manager):
    """
        This class is the manager of favorite model
    """

    def get_favorites_from_user(self, user):
        """
        This method returns favorite of a particular user
        """
        return self.filter(user=user)
