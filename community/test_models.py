from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.urls import reverse
from django.test import TestCase

from .models import MessagePost, MessageTopic


class CommunityModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )
        self.topic = MessageTopic.objects.create(
            subject='Test Create Topic',
            started_by=self.user,
        )
        self.post = MessagePost.objects.create(
            message='Lorem ipsum dolor sit amet',
            topic=self.topic,
            created_by=self.user,
        )
        self.other_user = get_user_model().objects.create_user(
            username='otheruser',
            email='other@email.com',
            password='secret2'
        )

    def test_reply_post_view_logged_in(self):
        self.client.login(
            username='testuser',
            password='secret',
        )
        test_topic = MessageTopic.objects.get(subject='Test Create Topic')
        response = self.client.post(reverse(
            'reply_post',
            kwargs={'topic_id': test_topic.id}), {
            'message': 'New message post',
            'created_by': self.user,
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New message post')
        self.assertTemplateUsed(response, 'community/view_topic.html')

    def test_post_reply_view_not_logged_in(self):
        test_topic = MessageTopic.objects.get(subject='Test Create Topic')
        response = self.client.post(reverse(
            'reply_post',
            kwargs={'topic_id': test_topic.id}), {
            'message': 'New message post',
            'created_by': self.user,
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign In')

    def test_reply_post_get_page_logged_in(self):
        self.client.login(
            username='testuser',
            password='secret',
        )
        test_topic = MessageTopic.objects.get(subject='Test Create Topic')
        response = self.client.get(reverse(
            'reply_post',
            kwargs={'topic_id': test_topic.id}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'Reply to {test_topic}')
        self.assertTemplateUsed(response, 'community/reply_topic.html')

    def test_edit_post_view_logged_in(self):
        self.client.login(
            username='testuser',
            password='secret',
        )
        test_topic = MessageTopic.objects.get(subject='Test Create Topic')
        test_post = MessagePost.objects.get(
            message='Lorem ipsum dolor sit amet')
        response = self.client.post(reverse(
            'edit_post',
            kwargs={
                'topic_id': test_topic.id,
                'post_id': test_post.id,
            }), {
                'message': 'Edited message post',
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edited message post')
        self.assertTemplateUsed(response, 'community/view_topic.html')

    def test_edit_post_get_page_logged_in(self):
        self.client.login(
            username='testuser',
            password='secret',
        )
        test_topic = MessageTopic.objects.get(subject='Test Create Topic')
        test_post = MessagePost.objects.get(
            message='Lorem ipsum dolor sit amet')
        response = self.client.get(reverse(
            'edit_post',
            kwargs={
                'topic_id': test_topic.id,
                'post_id': test_post.id,
            })
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'Edit to {test_topic}')
        self.assertTemplateUsed(response, 'community/edit_post.html')

    def test_edit_post_view_not_logged_in(self):
        test_topic = MessageTopic.objects.get(subject='Test Create Topic')
        test_post = MessagePost.objects.get(
            message='Lorem ipsum dolor sit amet')
        response = self.client.post(reverse(
            'edit_post',
            kwargs={
                'topic_id': test_topic.id,
                'post_id': test_post.id,
            }), {
                'message': 'Edited message post',
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign In')

    def test_edit_post_of_other_user(self):
        self.client.login(
            username='otheruser',
            password='secret2',
        )
        test_topic = MessageTopic.objects.get(subject='Test Create Topic')
        test_post = MessagePost.objects.get(
            message='Lorem ipsum dolor sit amet')
        response = self.client.post(reverse(
            'edit_post',
            kwargs={
                'topic_id': test_topic.id,
                'post_id': test_post.id,
            }), {
                'message': 'Edited message post',
            },
            follow=True
        )
        messages = list(get_messages(response.wsgi_request))
        expected_message = ('This is not your post, you cannot edit it.')
        self.assertEqual(messages[0].tags, 'error')
        self.assertEqual(str(messages[0]), expected_message)
        self.assertRedirects(response, reverse(
            'view_topic',
            kwargs={
                'topic_id': test_topic.id,
            }),
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_post_view_logged_in(self):
        self.client.login(
            username='testuser',
            password='secret',
        )
        test_topic = MessageTopic.objects.get(subject='Test Create Topic')
        test_post = MessagePost.objects.get(
            message='Lorem ipsum dolor sit amet')
        response = self.client.post(reverse(
            'delete_post',
            kwargs={
                'topic_id': test_topic.id,
                'post_id': test_post.id,
            }),
            follow=True
        )
        messages = list(get_messages(response.wsgi_request))
        expected_message = ('Message deleted!')
        self.assertEqual(messages[0].tags, 'success')
        self.assertEqual(str(messages[0]), expected_message)
        self.assertRedirects(response, reverse(
            'view_topic',
            kwargs={
                'topic_id': test_topic.id,
            }),
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_post_of_other_user(self):
        self.client.login(
            username='otheruser',
            password='secret2',
        )
        test_topic = MessageTopic.objects.get(subject='Test Create Topic')
        test_post = MessagePost.objects.get(
            message='Lorem ipsum dolor sit amet')
        response = self.client.post(reverse(
            'delete_post',
            kwargs={
                'topic_id': test_topic.id,
                'post_id': test_post.id,
            }),
            follow=True
        )
        messages = list(get_messages(response.wsgi_request))
        expected_message = ('This is not your post, you cannot delete it.')
        self.assertEqual(messages[0].tags, 'error')
        self.assertEqual(str(messages[0]), expected_message)
        self.assertRedirects(response, reverse(
            'view_topic',
            kwargs={
                'topic_id': test_topic.id,
            }),
        )
        self.assertEqual(response.status_code, 200)
