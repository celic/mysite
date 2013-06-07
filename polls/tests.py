import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from polls.models import Poll

def create_poll(question, days):
	return Poll.objects.create(question = question, pub_date = timezone.now() + datetime.timedelta(days = days))

class PollsViewTests(TestCase):

	def test_index_view_with_no_polls(self):
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls available.")
		self.assertQuerysetEqual(response.context['latest_poll_list'], [])

	def test_index_view_with_a_past_poll(self):
		create_poll(question = "Past Poll", days = -30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_poll_list'], ['<Poll: Past Poll>']
		)

	def test_index_view_with_a_future_poll(self):
		create_poll(question = "Future Poll", days = 30)
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response, "No polls available.", status_code = 200)
		self.assertQuerysetEqual(response.context['latest_poll_list'], [])

	def test_index_view_with_future_poll_and_past_poll(self):
		create_poll(question = "Past Poll", days = -30)
		create_poll(question = "Future Poll", days = 30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_poll_list'], ['<Poll: Past Poll>']
		)

	def test_index_view_with_multiple_past_polls(self):
		create_poll(question = "Past Poll 1", days = -30)
		create_poll(question = "Past Poll 2", days = -30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_poll_list'], ['<Poll: Past Poll 2>', '<Poll: Past Poll 1>']
		)

class PollsMethodTests(TestCase):

	def test_was_published_recently_with_future_poll(self):
		"""
		Tests was_published_recently() with a future date
		to ensure it returns false
		"""
		future_poll = Poll(pub_date = timezone.now() + datetime.timedelta(days = 30))
		self.assertEqual(future_poll.was_published_recently(), False)

	def test_was_published_recently_with_old_poll(self):
		"""
		Tests was_published_recently() with an old date
		to ensure it returns false
		"""
		old_poll = Poll(pub_date = timezone.now() - datetime.timedelta(days = 30))
		self.assertEqual(old_poll.was_published_recently(), False)

	def test_was_published_recently_with_recent_poll(self):
		"""
		Tests was_published_recently() with a recent date
		to ensure it returns true
		"""
		recent_poll = Poll(pub_date = timezone.now() - datetime.timedelta(hours = 1))
		self.assertEqual(recent_poll.was_published_recently(), True)
