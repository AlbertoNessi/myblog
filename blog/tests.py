from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from .models import ProfileContent


class LlmsTxtViewTests(SimpleTestCase):
    def test_llms_txt_is_available_as_plain_text(self):
        response = self.client.get("/llms.txt")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response["Content-Type"].startswith("text/plain"))

    def test_llms_txt_describes_main_public_routes(self):
        response = self.client.get("/llms.txt")
        content = response.content.decode("utf-8")

        self.assertIn("Alberto Nessi Personal Website", content)
        self.assertIn("https://albertonessi.it/", content)
        self.assertIn("https://albertonessi.it/now", content)
        self.assertIn("https://albertonessi.it/reading", content)
        self.assertIn("https://albertonessi.it/quotes", content)


class ProfileContentTests(TestCase):
    def test_both_text_fields_are_required(self):
        profile = ProfileContent(introduction="", body="")

        with self.assertRaises(ValidationError) as error:
            profile.full_clean()

        self.assertIn("introduction", error.exception.message_dict)
        self.assertIn("body", error.exception.message_dict)

    def test_database_allows_only_the_singleton_id(self):
        ProfileContent.objects.create(introduction="Intro", body="Body")

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ProfileContent.objects.create(
                    id=2, introduction="Another intro", body="Another body"
                )

        self.assertEqual(ProfileContent.objects.count(), 1)


class ProfileContentAdminTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="profile-editor", password="test-password", email="editor@example.com"
        )
        self.client.force_login(self.user)

    def test_profile_can_be_created_once_and_edited_but_not_deleted(self):
        add_url = reverse("admin:blog_profilecontent_add")
        add_form = self.client.get(add_url)
        self.assertEqual(add_form.status_code, 200)
        self.assertNotContains(add_form, 'name="_addanother"')

        response = self.client.post(
            add_url,
            {"introduction": "Introduction", "body": "First paragraph\n\nSecond paragraph", "_save": "Save"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ProfileContent.objects.count(), 1)

        self.assertEqual(self.client.get(add_url).status_code, 403)
        change_url = reverse("admin:blog_profilecontent_change", args=[1])
        self.assertEqual(self.client.get(change_url).status_code, 200)
        self.assertEqual(self.client.get(reverse("admin:blog_profilecontent_delete", args=[1])).status_code, 403)

    def test_admin_rejects_empty_content(self):
        response = self.client.post(
            reverse("admin:blog_profilecontent_add"),
            {"introduction": "", "body": "", "_save": "Save"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(ProfileContent.objects.exists())


class ProfilePageTests(TestCase):
    def test_profile_renders_text_from_database_as_paragraphs(self):
        profile = ProfileContent.objects.create(
            introduction="Current introduction",
            body="First paragraph\r\n\r\nSecond paragraph",
        )

        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<p>Current introduction</p>", html=True)
        self.assertContains(response, "<p>First paragraph</p>", html=True)
        self.assertContains(response, "<p>Second paragraph</p>", html=True)

        profile.introduction = "Updated introduction"
        profile.save(update_fields=["introduction"])
        updated_response = self.client.get(reverse("index"))
        self.assertContains(updated_response, "Updated introduction")
        self.assertNotContains(updated_response, "Current introduction")

    def test_profile_escapes_html_from_database(self):
        ProfileContent.objects.create(
            introduction="<script>alert('x')</script>",
            body="<strong>Plain text</strong>",
        )

        response = self.client.get(reverse("index"))

        self.assertNotContains(response, "<script>")
        self.assertNotContains(response, "<strong>")
        self.assertContains(response, "&lt;script&gt;")
        self.assertContains(response, "&lt;strong&gt;")

    def test_profile_missing_record_is_not_hidden_by_a_fallback(self):
        with self.assertRaises(ProfileContent.DoesNotExist):
            self.client.get(reverse("index"))
