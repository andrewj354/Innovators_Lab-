import pytest
from django.utils import timezone
from datetime import timedelta
from apps.submissions.models import Submission, JuryAssignment, Score, Leaderboard


@pytest.mark.django_db
class TestSubmissionModel:
    """Тести для моделі Submission"""
    
    def test_create_submission(self):
        """Тест створення подачі"""
        submission = Submission.objects.create(
            task_id=1,
            team_id=1,
            github_url='https://github.com/test/repo',
            video_url='https://youtube.com/watch?v=123',
            live_demo_url='https://demo.example.com',
            description='Test submission'
        )
        
        assert submission.task_id == 1
        assert submission.team_id == 1
        assert not submission.is_locked
        assert submission.can_edit
    
    def test_submission_unique_per_task_team(self):
        """Тест унікальності подачі на завдання"""
        Submission.objects.create(
            task_id=1, team_id=1,
            github_url='https://github.com/test/repo1'
        )
        
        with pytest.raises(Exception):  # IntegrityError
            Submission.objects.create(
                task_id=1, team_id=1,
                github_url='https://github.com/test/repo2'
            )
    
    def test_submission_lock_unlock(self):
        """Тест блокування/розблокування подачі"""
        submission = Submission.objects.create(
            task_id=1, team_id=1,
            github_url='https://github.com/test/repo'
        )
        
        assert submission.can_edit
        
        submission.lock()
        assert not submission.can_edit
        assert submission.is_locked
        
        submission.unlock()
        assert submission.can_edit
        assert not submission.is_locked
    
    def test_submission_has_all_urls(self):
        """Тест перевірки всіх URL"""
        # Без всіх URL
        submission1 = Submission.objects.create(
            task_id=1, team_id=1,
            github_url='https://github.com/test/repo'
        )
        assert not submission1.has_all_urls()
        
        # З всіма URL
        submission2 = Submission.objects.create(
            task_id=2, team_id=2,
            github_url='https://github.com/test/repo',
            video_url='https://youtube.com/watch?v=123',
            live_demo_url='https://demo.example.com'
        )
        assert submission2.has_all_urls()


@pytest.mark.django_db
class TestJuryAssignmentModel:
    """Тести для моделі JuryAssignment"""
    
    @pytest.fixture
    def submission(self):
        """Фікстура для подачі"""
        return Submission.objects.create(
            task_id=1, team_id=1,
            github_url='https://github.com/test/repo'
        )
    
    def test_create_jury_assignment(self, submission):
        """Тест призначення журі"""
        assignment = JuryAssignment.objects.create(
            submission=submission,
            jury_user_id=5,
            is_evaluated=False
        )
        
        assert assignment.submission == submission
        assert assignment.jury_user_id == 5
        assert not assignment.is_evaluated
    
    def test_jury_assignment_unique(self, submission):
        """Тест унікальності призначення"""
        JuryAssignment.objects.create(
            submission=submission, jury_user_id=5
        )
        
        with pytest.raises(Exception):  # IntegrityError
            JuryAssignment.objects.create(
                submission=submission, jury_user_id=5
            )
    
    def test_mark_as_evaluated(self, submission):
        """Тест позначення як оцінене"""
        assignment = JuryAssignment.objects.create(
            submission=submission, jury_user_id=5
        )
        
        assert not assignment.is_evaluated
        assignment.mark_as_evaluated()
        assert assignment.is_evaluated


@pytest.mark.django_db
class TestScoreModel:
    """Тести для моделі Score"""
    
    @pytest.fixture
    def assignment(self):
        """Фікстура для призначення журі"""
        submission = Submission.objects.create(
            task_id=1, team_id=1,
            github_url='https://github.com/test/repo'
        )
        return JuryAssignment.objects.create(
            submission=submission, jury_user_id=5
        )
    
    def test_create_score(self, assignment):
        """Тест створення оцінки"""
        score = Score.objects.create(
            assignment=assignment,
            backend_code=85,
            database=90,
            frontend_code=80,
            functionality=95,
            usability=88,
            comment='Good work'
        )
        
        assert score.backend_code == 85
        assert score.database == 90
        assert score.assignment == assignment
    
    def test_score_average(self, assignment):
        """Тест обчислення середної оцінки"""
        score = Score.objects.create(
            assignment=assignment,
            backend_code=80,
            database=80,
            frontend_code=80,
            functionality=80,
            usability=80
        )
        
        assert score.average_score == 80.0
    
    def test_score_total(self, assignment):
        """Тест обчислення загальної оцінки"""
        score = Score.objects.create(
            assignment=assignment,
            backend_code=85,
            database=90,
            frontend_code=80,
            functionality=95,
            usability=88
        )
        
        assert score.total_score == 85 + 90 + 80 + 95 + 88
    
    def test_score_validation(self, assignment):
        """Тест валідації оцінок"""
        # Оцінки повинні бути від 0 до 100
        with pytest.raises(Exception):  # ValidationError
            Score.objects.create(
                assignment=assignment,
                backend_code=101,  # > 100
                database=50,
                frontend_code=50,
                functionality=50,
                usability=50
            )
    
    def test_score_unique_per_assignment(self, assignment):
        """Тест унікальності оцінки на призначення"""
        Score.objects.create(
            assignment=assignment,
            backend_code=85, database=90, frontend_code=80,
            functionality=95, usability=88
        )
        
        with pytest.raises(Exception):  # IntegrityError
            Score.objects.create(
                assignment=assignment,
                backend_code=75, database=80, frontend_code=70,
                functionality=85, usability=78
            )


@pytest.mark.django_db
class TestLeaderboardModel:
    """Тести для моделі Leaderboard"""
    
    def test_create_leaderboard_entry(self):
        """Тест створення запису в лідербордом"""
        entry = Leaderboard.objects.create(
            tournament_id=1,
            team_id=1,
            total_score=425.0,
            rank=1
        )
        
        assert entry.tournament_id == 1
        assert entry.team_id == 1
        assert entry.total_score == 425.0
        assert entry.rank == 1
    
    def test_leaderboard_unique_per_tournament(self):
        """Тест унікальності команди в лідербордом турніру"""
        Leaderboard.objects.create(
            tournament_id=1, team_id=1, total_score=425.0, rank=1
        )
        
        with pytest.raises(Exception):  # IntegrityError
            Leaderboard.objects.create(
                tournament_id=1, team_id=1, total_score=420.0, rank=2
            )
    
    def test_update_score(self):
        """Тест оновлення оцінки"""
        entry = Leaderboard.objects.create(
            tournament_id=1, team_id=1, total_score=100.0, rank=1
        )
        
        entry.update_score(250.0)
        
        assert entry.total_score == 250.0
    
    def test_leaderboard_ordering(self):
        """Тест впорядкування лідербордом"""
        Leaderboard.objects.create(
            tournament_id=1, team_id=1, total_score=500.0, rank=1
        )
        Leaderboard.objects.create(
            tournament_id=1, team_id=2, total_score=450.0, rank=2
        )
        Leaderboard.objects.create(
            tournament_id=1, team_id=3, total_score=400.0, rank=3
        )
        
        entries = Leaderboard.objects.filter(tournament_id=1)
        
        assert entries[0].rank == 1
        assert entries[1].rank == 2
        assert entries[2].rank == 3
