from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
import re

from lists.views import home_page
from lists.models import Item, List

class HomePageTest(TestCase):
    def remove_csrf(self, origin):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', origin)

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        expected_html = self.remove_csrf(render_to_string("home.html", request=request))
        response_decode = self.remove_csrf(response.content.decode())

        self.assertEqual (response_decode, expected_html)
        
class ListAndItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        
        first_item = Item()
        first_item.text = "첫 번째 아이템"
        first_item.list = list_
        first_item.save()
        
        second_item = Item()
        second_item.text = "두 번째 아이템"
        second_item.list = list_
        second_item.save()
        
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "첫 번째 아이템")
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, "두 번째 아이템")
        self.assertEqual(second_saved_item.list, list_)
        
class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get("/lists/the-only-list-in-the-world")
        self.assertTemplateUsed(response, "list.html")
        
    def test_home_page_displays_all_list_items(self):
        lists_ = List.objects.create()
        Item.objects.create(text="itemey 1", list=lists_)
        Item.objects.create(text="itemey 2", list=lists_)
        
        response = self.client.get("/lists/the-only-list-in-the-world")

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
        
class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post("/lists/new", data={"item_text": "신규 작업 아이템"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "신규 작업 아이템")
        
    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={"item_text": "신규 작업 아이템"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/lists/the-only-list-in-the-world")