from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Submission


class SubmissionModelTest(TestCase):
    """Test Submission model"""
    
    def setUp(self):
        self.submission = Submission.objects.create(
            task_id=1,
            team_id=1,
            code="print('hello')",
            language="python",
            status=Submission.Status.SUBMITTED,
            passed_tests=0,
            total_tests=5,
            score=0.0
        )
    
    def test_submission_creation(self):
        self.assertEqual(self.submission.code, "print('hello')")
        self.assertEqual(self.submission.language, "python")
        self.assertEqual(self.submission.status, "submitted")
    
    def test_submission_lock(self):
        self.submission.is_locked = True
        self.submission.save()
        self.assertTrue(self.submission.is_locked)
