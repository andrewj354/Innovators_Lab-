import pytest
from django.utils import timezone
from datetime import timedelta
from apps.tournaments.models import User, Tournament, Team, TeamMember, Task, TaskRequirement


@pytest.mark.django_db
class TestUserModel:
    """Тести для моделі User"""
    
    def test_create_user(self):
        """Тест створення користувача"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            name='Test User',
            password='testpass123',
            role=User.Role.TEAM_LEAD
        )
        
        assert user.email == 'test@example.com'
        assert user.name == 'Test User'
        assert user.role == User.Role.TEAM_LEAD
        assert user.is_team_lead()
    
    def test_user_unique_email(self):
        """Тест унікальності email"""
        User.objects.create_user(
            username='user1',
            email='same@example.com',
            name='User 1',
            password='pass123'
        )
        
        with pytest.raises(Exception):  # IntegrityError
            User.objects.create_user(
                username='user2',
                email='same@example.com',
                name='User 2',
                password='pass123'
            )
    
    def test_user_roles(self):
        """Тест різних ролей користувача"""
        admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            name='Admin',
            password='pass',
            role=User.Role.ADMIN
        )
        
        jury = User.objects.create_user(
            username='jury',
            email='jury@example.com',
            name='Jury',
            password='pass',
            role=User.Role.JURY
        )
        
        assert admin.is_admin()
        assert not admin.is_jury()
        assert jury.is_jury()
        assert not jury.is_team_lead()


@pytest.mark.django_db
class TestTournamentModel:
    """Тести для моделі Tournament"""
    
    @pytest.fixture
    def admin_user(self):
        """Фікстура для адміністратора"""
        return User.objects.create_user(
            username='admin',
            email='admin@example.com',
            name='Admin',
            password='admin123',
            role=User.Role.ADMIN
        )
    
    def test_create_tournament(self, admin_user):
        """Тест створення турніру"""
        now = timezone.now()
        tournament = Tournament.objects.create(
            created_by=admin_user,
            title='Test Tournament',
            description='Test Description',
            reg_start=now,
            reg_end=now + timedelta(days=7),
            max_teams=10,
            status=Tournament.Status.REGISTRATION
        )
        
        assert tournament.title == 'Test Tournament'
        assert tournament.created_by == admin_user
        assert tournament.max_teams == 10
    
    def test_tournament_registration_open(self, admin_user):
        """Тест перевірки відкритої реєстрації"""
        now = timezone.now()
        
        # Реєстрація відкрита
        tournament_open = Tournament.objects.create(
            created_by=admin_user,
            title='Open Registration',
            description='Test',
            reg_start=now - timedelta(hours=1),
            reg_end=now + timedelta(days=7),
            max_teams=10,
            status=Tournament.Status.REGISTRATION
        )
        
        # Реєстрація закрита
        tournament_closed = Tournament.objects.create(
            created_by=admin_user,
            title='Closed Registration',
            description='Test',
            reg_start=now - timedelta(days=10),
            reg_end=now - timedelta(days=1),
            max_teams=10,
            status=Tournament.Status.RUNNING
        )
        
        assert tournament_open.is_registration_open
        assert not tournament_closed.is_registration_open
    
    def test_tournament_can_accept_teams(self, admin_user):
        """Тест перевірки можливості приймання команд"""
        now = timezone.now()
        tournament = Tournament.objects.create(
            created_by=admin_user,
            title='Tournament',
            description='Test',
            reg_start=now - timedelta(hours=1),
            reg_end=now + timedelta(days=7),
            max_teams=2,
            status=Tournament.Status.REGISTRATION
        )
        
        # Спочатку може приймати
        assert tournament.can_accept_teams()
        
        # Додаємо команди до максимуму
        Team.objects.create(
            tournament=tournament,
            name='Team 1',
            captain_name='Captain 1',
            captain_email='cap1@example.com',
            city='Kyiv',
            contact='+380123456789'
        )
        Team.objects.create(
            tournament=tournament,
            name='Team 2',
            captain_name='Captain 2',
            captain_email='cap2@example.com',
            city='Lviv',
            contact='+380987654321'
        )
        
        # Тепер не може приймати (досягнута максимальна кількість)
        assert not tournament.can_accept_teams()


@pytest.mark.django_db
class TestTeamModel:
    """Тести для моделі Team"""
    
    @pytest.fixture
    def tournament(self):
        """Фікстура для турніру"""
        admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            name='Admin',
            password='pass',
            role=User.Role.ADMIN
        )
        now = timezone.now()
        return Tournament.objects.create(
            created_by=admin,
            title='Test Tournament',
            description='Test',
            reg_start=now,
            reg_end=now + timedelta(days=7),
            max_teams=10,
            status=Tournament.Status.REGISTRATION
        )
    
    def test_create_team(self, tournament):
        """Тест створення команди"""
        team = Team.objects.create(
            tournament=tournament,
            name='Test Team',
            captain_name='Captain',
            captain_email='captain@example.com',
            city='Kyiv',
            contact='+380123456789'
        )
        
        assert team.name == 'Test Team'
        assert team.tournament == tournament
        assert team.members_count == 0
    
    def test_team_unique_name_per_tournament(self, tournament):
        """Тест унікальності назви команди в турнірі"""
        Team.objects.create(
            tournament=tournament,
            name='Unique Team',
            captain_name='Captain 1',
            captain_email='cap1@example.com',
            city='Kyiv',
            contact='+380123456789'
        )
        
        with pytest.raises(Exception):  # IntegrityError
            Team.objects.create(
                tournament=tournament,
                name='Unique Team',
                captain_name='Captain 2',
                captain_email='cap2@example.com',
                city='Lviv',
                contact='+380987654321'
            )


@pytest.mark.django_db
class TestTeamMemberModel:
    """Тести для моделі TeamMember"""
    
    @pytest.fixture
    def team(self):
        """Фікстура для команди"""
        admin = User.objects.create_user(
            username='admin', email='admin@example.com',
            name='Admin', password='pass', role=User.Role.ADMIN
        )
        now = timezone.now()
        tournament = Tournament.objects.create(
            created_by=admin, title='Tournament', description='Test',
            reg_start=now, reg_end=now + timedelta(days=7),
            max_teams=10, status=Tournament.Status.REGISTRATION
        )
        return Team.objects.create(
            tournament=tournament, name='Team', captain_name='Captain',
            captain_email='cap@example.com', city='Kyiv', contact='+380123456789'
        )
    
    def test_add_team_member(self, team):
        """Тест додавання члена команди"""
        member = TeamMember.objects.create(
            team=team,
            full_name='Member Name',
            email='member@example.com'
        )
        
        assert member.full_name == 'Member Name'
        assert team.members_count == 1
    
    def test_team_member_unique_email_per_team(self, team):
        """Тест унікальності email у команді"""
        TeamMember.objects.create(
            team=team, full_name='Member 1', email='same@example.com'
        )
        
        with pytest.raises(Exception):  # IntegrityError
            TeamMember.objects.create(
                team=team, full_name='Member 2', email='same@example.com'
            )


@pytest.mark.django_db
class TestTaskModel:
    """Тести для моделі Task"""
    
    @pytest.fixture
    def task(self):
        """Фікстура для завдання"""
        admin = User.objects.create_user(
            username='admin', email='admin@example.com',
            name='Admin', password='pass', role=User.Role.ADMIN
        )
        now = timezone.now()
        tournament = Tournament.objects.create(
            created_by=admin, title='Tournament', description='Test',
            reg_start=now, reg_end=now + timedelta(days=7),
            max_teams=10, status=Tournament.Status.REGISTRATION
        )
        return Task.objects.create(
            tournament=tournament, created_by=admin,
            title='Test Task', description='Task description',
            tech_requirements='Python, Django',
            start_time=now, deadline=now + timedelta(days=3),
            status=Task.Status.PUBLISHED
        )
    
    def test_create_task(self, task):
        """Тест створення завдання"""
        assert task.title == 'Test Task'
        assert task.status == Task.Status.PUBLISHED
    
    def test_task_is_active(self, task):
        """Тест перевірки активного завдання"""
        # Завдання активно (тепер в межах часу)
        assert task.is_active
        
        # Завдання неактивно (дедлайн минув)
        task.deadline = timezone.now() - timedelta(hours=1)
        task.save()
        assert not task.is_active
    
    def test_task_submissions_count(self, task):
        """Тест підрахунку подач"""
        assert task.submissions_count == 0


@pytest.mark.django_db
class TestTaskRequirementModel:
    """Тести для моделі TaskRequirement"""
    
    @pytest.fixture
    def task(self):
        """Фікстура для завдання"""
        admin = User.objects.create_user(
            username='admin', email='admin@example.com',
            name='Admin', password='pass', role=User.Role.ADMIN
        )
        now = timezone.now()
        tournament = Tournament.objects.create(
            created_by=admin, title='Tournament', description='Test',
            reg_start=now, reg_end=now + timedelta(days=7),
            max_teams=10, status=Tournament.Status.REGISTRATION
        )
        return Task.objects.create(
            tournament=tournament, created_by=admin,
            title='Task', description='Test', tech_requirements='',
            start_time=now, deadline=now + timedelta(days=3),
            status=Task.Status.PUBLISHED
        )
    
    def test_create_requirement(self, task):
        """Тест створення вимоги"""
        req = TaskRequirement.objects.create(
            task=task,
            title='REST API required',
            is_required=True
        )
        
        assert req.title == 'REST API required'
        assert req.is_required
        assert task.requirements.count() == 1
    
    def test_optional_requirement(self, task):
        """Тест опціональної вимоги"""
        req = TaskRequirement.objects.create(
            task=task,
            title='Docker support',
            is_required=False
        )
        
        assert not req.is_required
