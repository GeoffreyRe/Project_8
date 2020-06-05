"""
This module contains tests of app 'favorites'
"""
import io
import json
import unittest.mock as u
from django.test import TestCase, Client
from users.models import User
from products.models import Product, Category
from .models import Favorite
from django.contrib.auth import logout
from django.core.files.uploadedfile import SimpleUploadedFile
import favorites.import_export_favorites as utils


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

    def test_import_json_file_adds_favorites(self):
        p3 = Product.objects.create(barcode="123456",
                                    product_name="Lait3",
                                    brand="gandia +",
                                    url_page="www.test.com",
                                    image_url="www.image-test.com",
                                    image_nutrition_url="www.nut-image.com",
                                    nutrition_grade="A",
                                    nutrition_score=1,
                                    category=self.cat)
        file_content = b'[{"test": "123"}, {"Code barre produit" :"1234", "Code barre substitut" : "123456"}]'
        imported_file = SimpleUploadedFile("my_favs.json", file_content, content_type="application/json")
        # we simulate an upload of a json file with some content inside
        response = self.client.post("/favorite/import", {"imported_file" : imported_file}, follow=True)
        # if everything goes well, a new favorite should be added
        expected = ["Lait1 remplacé par Lait2", "Lait1 remplacé par Lait3"]
        user_favorites = Favorite.objects.get_favorites_from_user(self.user1)
        self.assertTrue(
            all(str(a) == b for a, b in zip(user_favorites, expected)))
        # we make sure good messages are delivered
        for message in response.context['messages']:
            self.assertIn(str(message), ["le ou les favoris suivants ont été ajoutés : produit 1234/ substitut 123456, ",
                                    "au moins un couple produit/substitut n'a pas été ajouté car sa structure n'est pas correcte"])


class FavoritesUtilsTest(TestCase):
    """
    This class contains tests of views of 'favorites' application
    """

    def setUp(self):
        """
        This function is executed each time a new test function is executed
        """
        self.user1 = User.objects.create_user(username="Michello", password="1234",
                                              email="test@test.com")
        self.client = Client()

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
                                         product_name="Lait3",
                                         brand="gandia",
                                         url_page="www.test.com",
                                         image_url="www.image-test.com",
                                         image_nutrition_url="www.nut-image.com",
                                         nutrition_grade="A",
                                         nutrition_score=0,
                                         category=self.cat)
        Favorite.objects.create(
            user=self.user1, product=self.p1, substitute=self.p2)

    def test_serialize_favorites_from_user_return_a_json_obj_with_user_favorites(self):
        # we will check if function returns favorites of user in json format
        json_fav = utils.serialize_favorites_from_user(self.user1)
        excpected_json = {
            "Code barre produit": "1234" ,
            "Nom produit": "Lait1",
            "Marque produit" : "Lactel",
            "Code barre substitut" : "12345",
            "Nom substitut" : "Lait2",
            "Marque substitut" : "gandia"
        }
        self.assertEqual(json_fav, json.dumps([excpected_json], indent=4).encode("utf8"))

    def test_find_favorites_from_json_returns_error_message_if_json_not_valid(self):
        # in this example, json format is not valid because a bracket is missing at the end
        raw_datas = b'[{"code barre" : 1}'
        output = utils.find_favorites_from_json(raw_datas)
        self.assertEqual(output, (False, "Fichier Json non valide"))
    
    def test_find_favorites_from_json_returns_error_message_if_format_not_valid(self):
        # in this example, json format is valid but
        # we excpected a list and not an other python object
        raw_datas = b'{"code barre" : 1}'
        output = utils.find_favorites_from_json(raw_datas)
        self.assertEqual(output, (False, "la structure du fichier json n'est pas correcte"))

    def test_find_favorites_from_json_returns_error_message_if_format_of_fav_not_valid(self):
        # in this example, json format is valid but
        # we excpected a dict for every favorite to append
        # so, in this case, a list of lists is not good
        raw_datas = b'[["code barre"], ["code barre"]]'
        output = utils.find_favorites_from_json(raw_datas)
        self.assertEqual(output, (False, "la structure du fichier json n'est pas correcte"))

    def test_find_favorites_from_json_returns_error_message_if_key_of_fav_not_valid(self):
        # in this example, json format is valid but
        # we excpected a name for keys
        # so, in this case, keys like "Code barre" is not good
        # and this favorite will be skipped and not append to final favs to add
        raw_datas = b'[{"Code barre produit" : "1234567", "Code barre substitut" :"11"}, {"Code barre" : "1111"}]'
        output = utils.find_favorites_from_json(raw_datas)
        self.assertEqual(output, (True,
        "au moins un couple produit/substitut n'a pas été ajouté car sa structure n'est pas correcte",
        [("1234567", "11")]))

    def test_find_favorites_from_json_returns_favs_if_everything_ok(self):
        # in this example, json format is valid and everything else like keys etc...
        # are valid too so the function will returns barcodes of favorites

        raw_datas = (b'[{"Code barre produit" : "1234567", "Code barre substitut" :"11"}, '
                    b'{"Code barre produit" : "1111", "Code barre substitut" : "1234"}]')
        output = utils.find_favorites_from_json(raw_datas)
        self.assertEqual(output, [("1234567", "11"), ("1111", "1234")])

    def test_generate_messages_create_good_messages(self):
            messages_list = utils.generate_messages([('1', '2')], [('0', '1')], [])
            self.assertEqual(messages_list[0], "le ou les favoris suivants ont été ajoutés : produit 1/ substitut 2, ")
            self.assertEqual(messages_list[1], ("le ou les favoris suivants étaient déjà "
                                                "enregistrés en tant que favoris : "
                                                "produit 0/ substitut 1, "))

    def test_add_favorites_from_json_add_fav_to_user_and_add_not_products_already_saved(self):
        # we have to log the user to the session
        # This user has already product p1 and p2 as fav
        user_id = self.user1.id
        # we create mocks
        class MockSession:
                def get(self, id):
                    return user_id
        class MockRequest:
            def __init__(self):
                self.session = MockSession()
        # in this list, the first one is already saved, the second one must be saved
        # and the thrid one does not exist
        fav_to_add = [(self.p1.barcode, self.p2.barcode),
                    ('barcode non valide', 'barcode non valide aussi',
                    (self.p1.barcode, self.p3.barcode))
                    ]
        fav_of_user = Favorite.objects.get_favorites_from_user(self.user1)
        utils.add_favorites_from_json(MockRequest(), fav_to_add)
        expected = ["Lait1 remplacé par Lait2", "Lait1 remplacé par Lait3"]
        # if everything goes well, the user should have a new favorite added, p1 and p3
        self.assertTrue(
            all(str(a) == b for a, b in zip(fav_of_user, expected)))

    @u.patch('django.contrib.messages.error')
    def test_file_is_imported_and_is_json_returns_False_if_not_file(self, mockError):
        # in this case, if FILES has not "imported_file" attribute, 
        # it means that there is no file in POST request and so this function
        # has to return False
        class MockRequest:
            def __init__(self):
                self.FILES = {}
        response = utils.file_imported_and_is_json(MockRequest())
        self.assertIs(response, False)

    @u.patch('django.contrib.messages.error')
    def test_file_is_imported_and_is_json_returns_False_if_not_json_file(self, mockError):
        """
        In this case, if a file is well imported but this is not a json file, this function
        has to return False
        """
        class MockFile:
            def __init__(self):
                self.name = "fav.txt"
        class MockRequest:
            def __init__(self):
                self.FILES = {"imported_file" : MockFile()}
        response = utils.file_imported_and_is_json(MockRequest())
        self.assertIs(response, False)


    def test_file_is_imported_and_is_json_returns_file_instance_if_json_file(self):
        """
        In this case, if a file is well imported and is of type json, the function
        has to return instance of file
        """
        class MockFile:
            def __init__(self):
                self.name = "fav.json"
        class MockRequest:
            def __init__(self):
                self.FILES = {"imported_file" : MockFile()}

        response = utils.file_imported_and_is_json(MockRequest())

        self.assertEqual(type(response), MockFile)
    @u.patch('django.contrib.messages.error')
    def test_analyse_fav_to_add_returns_list_if_everything_ok(self, mockError):
        """
        In this case, analyse_fav_to_add must return favs because,
        this is not a tuple and because favs is not empty
        """
        class MockRequest:
            pass
        favs = [('111', '1234'), ('123', '1234')]
        response = utils.analyse_fav_to_add(MockRequest(), favs)

        self.assertEqual(favs, response)

    @u.patch('django.contrib.messages.error')
    def test_analyse_fav_to_add_returns_False_if_tuple_and_false(self, MockError):
        """
        In this case, analyse_fav_to_add must return False because
        favs is a tuple with False in the first index
        """
        class MockRequest:
            pass
        favs = (False, "la structure du fichier json n'est pas correcte")
        response = utils.analyse_fav_to_add(MockRequest(), favs)

        self.assertIs(False, response)

    @u.patch('django.contrib.messages.error')
    @u.patch('django.contrib.messages.warning')
    def test_analyse_fav_to_add_returns_fav_list_if_tuple_and_true(self, MockWarning, MockError):
        """
        In this case, analyse_fav_to_add must return fav list because
        favs is a tuple with True in the first index
        """
        class MockRequest:
            pass
        fav_list = [('1111', '2121')]
        favs = (True, "Au moins un couple de favoris a un problème de structure",
                fav_list)
        response = utils.analyse_fav_to_add(MockRequest(), favs)

        self.assertEqual(fav_list, response)

    @u.patch('django.contrib.messages.error')
    def test_analyse_fav_to_add_returns_false_if_favs_to_add_is_empty(self, MockError):
        """
        In this case, analyse_fav_to_add has to return False because favs list is empty
        """
        class MockRequest:
            pass
        
        response = utils.analyse_fav_to_add(MockRequest(), [])
        self.assertIs(response, False)





