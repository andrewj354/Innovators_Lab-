from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Task, TaskRequirement


class TaskModelTest(TestCase):
    """Test Task model"""
    
    def setUp(self):
        self.task = Task.objects.create(
            tournament_id=1,
            title="Test Task",
            description="Test Description",
            difficulty=Task.Difficulty.MEDIUM,
            status=Task.Status.PUBLISHED,
            time_limit=60,
            memory_limit=256,
            points=100
        )
    
    def test_task_creation(self):
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.difficulty, "medium")


class TaskRequirementModelTest(TestCase):
    """Test TaskRequirement model"""
    
    def setUp(self):
        self.task = Task.objects.create(
            tournament_id=1,
            title="Test Task",
            description="Test Description",
            difficulty=Task.Difficulty.MEDIUM,
            status=Task.Status.PUBLISHED,
            time_limit=60,
            memory_limit=256,
            points=100
        )
        self.requirement = TaskRequirement.objects.create(
            task=self.task,
            input_data="1 2",
            expected_output="3",
            is_sample=True
        )
    
    def test_requirement_creation(self):
        self.assertEqual(self.requirement.input_data, "1 2")
        self.assertEqual(self.requirement.expected_output, "3")
