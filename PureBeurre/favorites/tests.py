"""
This module contains tests of app 'favorites'
"""
import io
import json
from django.test import TestCase, Client
from users.models import User
from products.models import Product, Category
from .models import Favorite
from django.contrib.auth import logout


# Create your tests here.
class FavoritesManagerTest(TestCase):
    """
    This class contains tests of views of 'favorites' application
    """

    def setUp(self):
        """
        This function is executed each time a new test function is executed
        """
        self.cat = Category.objects.create(name="Lait", parent_category=None)
        self.p1 = Product.objects.create(barcode="1234",
                                         product_name="Lait1",
                                         brand="Lactel",
                                         url_page="www.test.com",
                                         image_url="www.image-test.com",
                                         image_nutrition_url="www.nut-image.com",
                                         nutrition_grade="A",
                                         nutrition_score=5,
                                         category=self.cat)
        self.p2 = Product.objects.create(barcode="12345",
                                         product_name="Lait2",
                                         brand="gandia",
                                         url_page="www.test.com",
                                         image_url="www.image-test.com",
                                         image_nutrition_url="www.nut-image.com",
                                         nutrition_grade="A",
                                         nutrition_score=3,
                                         category=self.cat)
        self.p3 = Product.objects.create(barcode="123456",
                                         product_name="Lait BIO",
                                         brand="Matel",
                                         url_page="www.test.com",
                                         image_url="www.image-test.com",
                                         image_nutrition_url="www.nut-image.com",
                                         nutrition_grade="b",
                                         nutrition_score=12,
                                         category=self.cat)
        self.eric = User.objects.create_user('Eric', 'eric@test.com', '1111')
        self.mathieu = User.objects.create_user(
            'Mathieu', 'mathieu@test.com', '1112')
        Favorite.objects.create(
            user=self.eric, product=self.p1, substitute=self.p2)
        Favorite.objects.create(
            user=self.mathieu, product=self.p1, substitute=self.p3)

    def test_manager_method_return_set_of_favorites(self):
        """This method tests if manager method returns favorites"""
        fav_of_eric = Favorite.objects.get_favorites_from_user(self.eric)
        self.assertQuerysetEqual(fav_of_eric,
                                 set(["Lait1 remplacé par Lait2"]),
                                 ordered=False, transform=str)
        fav_of_mathieu = Favorite.objects.get_favorites_from_user(self.mathieu)
        self.assertQuerysetEqual(fav_of_mathieu,
                                 set(["Lait1 remplacé par Lait BIO"]),
                                 ordered=False, transform=str)


class FavoritesViewsTest(TestCase):
    """
    This class contains tests of views of 'favorites' application
    """

    def setUp(self):
        """
        This function is executed each time a new test function is executed
        """
        self.client = Client()
        self.user1 = User.objects.create_user(username="Michello", password="1234",
                                              email="test@test.com")
        self.client.login(username='Michello', password='1234')

        self.cat = Category.objects.create(name="Lait", parent_category=None)
        self.p1 = Product.objects.create(barcode="1234",
                                         product_name="Lait1",
                                         brand="Lactel",
                                         url_page="www.test.com",
                                         image_url="www.image-test.com",
                                         image_nutrition_url="www.nut-image.com",
                                         nutrition_grade="A",
                                         nutrition_score=5,
                                         category=self.cat)
        self.p2 = Product.objects.create(barcode="12345",
                                         product_name="Lait2",
                                         brand="gandia",
                                         url_page="www.test.com",
                                         image_url="www.image-test.com",
                                         image_nutrition_url="www.nut-image.com",
                                         nutrition_grade="A",
                                         nutrition_score=3,
                                         category=self.cat)
        Favorite.objects.create(
            user=self.user1, product=self.p1, substitute=self.p2)

    def test_user_favorites_returns_favorites_of_logged_user(self):
        """This method tests if user_favorites returns favorites of user"""
        response = self.client.get('/favorite/')
        fav_of_user = Favorite.objects.get_favorites_from_user(self.user1)
        self.assertEqual(response.status_code, 200)
        # we check if all element inside querysets are equal
        self.assertTrue(all(a == b for a, b in zip(
            fav_of_user, response.context['favorites'])))
        self.assertTemplateUsed(response, 'favorites/favorites.html')

    def test_user_favorites_redirect_user_if_not_logged(self):
        """This method tests if user_favorites view redirects user if not logged"""
        logout(self.client)
        response = self.client.get('/favorite/')
        self.assertEqual(response.status_code, 302)

    def test_add_favorites_add_favorite_to_favorites_of_user(self):
        """This method tests if add favorites work well"""
        p3 = Product.objects.create(barcode="123456",
                                    product_name="Lait3",
                                    brand="gandia +",
                                    url_page="www.test.com",
                                    image_url="www.image-test.com",
                                    image_nutrition_url="www.nut-image.com",
                                    nutrition_grade="A",
                                    nutrition_score=1,
                                    category=self.cat)
        self.client.get('/favorite/1234/123456')
        fav_of_user = Favorite.objects.get_favorites_from_user(self.user1)
        expected = ["Lait1 remplacé par Lait2", "Lait1 remplacé par Lait3"]
        self.assertTrue(
            all(str(a) == b for a, b in zip(fav_of_user, expected)))

    def test_add_favorites_redirect_user_if_not_logged(self):
        """"This method tests if add_favorites view redirects user if not logged"""
        logout(self.client)
        response = self.client.get('/favorite/1234/123456')
        self.assertEqual(response.status_code, 302)

    def test_add_favorites_redirect_user_if_favorites_already_in_dtb(self):
        """ This method tests if add_favorites view redirects user
        if favorite is already in database"""
        response = self.client.get('/favorite/1234/12345')
        self.assertEqual(response.status_code, 302)

    def test_export_favorites_from_user_returns_favorites_into_a_file(self):
        response = self.client.get('/favorite/export')
        # the name of the file has to be 'favorites' + name of user
        correct_filename = '"favorites_Michello.json"' in response.get("Content-Disposition")
        self.assertIs(correct_filename, True)
        json_obj = json.loads(response.content)
        user_favorite = Favorite.objects.all()[0]
        fav_infos = {}
        fav_infos["Code barre produit"] = user_favorite.product.barcode
        fav_infos["Nom produit"] = user_favorite.product.product_name
        fav_infos["Code barre substitut"] = user_favorite.substitute.barcode
        fav_infos["Nom substitut"] = user_favorite.substitute.product_name
        fav_infos["Marque substitut"] = user_favorite.substitute.brand
        fav_infos["Marque produit"] = user_favorite.product.brand
        # we checks if informations inside file is the same has informations about user's favorites
        self.assertEqual(json_obj, [fav_infos])
