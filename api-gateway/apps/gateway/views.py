import requests
import json
import logging
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views import View

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class ProxyView(View):


    def dispatch(self, request, *args, **kwargs):

        logger.info(f"Gateway request: {request.method} {request.path}")
        logger.info(f"Headers: {dict(request.headers)}")
        logger.info(f"Body: {request.body.decode('utf-8') if request.body else 'No body'}")


        service_name = self.get_service_name(request)
        if not service_name:
            logger.error(f"Service not found for path: {request.path}")
            return JsonResponse({'error': 'Service not found'}, status=404)


        service_url = settings.MICROSERVICES.get(service_name)
        if not service_url:
            logger.error(f"Service {service_name} not configured")
            return JsonResponse({'error': f'Service {service_name} not configured'}, status=500)


        target_path = self.get_target_path(request)
        target_url = f"{service_url}{target_path}"

        logger.info(f"Proxying to: {target_url}")


        return self.proxy_request(request, target_url)

    def get_service_name(self, request):
        """Определение сервиса по URL"""
        path = request.path

        # Auth & Users → user-service (8001)
        if path.startswith('/api/auth/') or path.startswith('/api/users/') or path.startswith('/api/teams/'):
            return 'user-service'
        
        # Tasks & Submissions → task-service (8002)
        elif path.startswith('/api/tasks/') or path.startswith('/api/submissions/'):
            return 'task-service'
        
        # Jury & Leaderboard → rank-service (8002, consolidated with task-service)
        elif path.startswith('/api/jury-assignments/') or path.startswith('/api/jury/') or path.startswith('/api/scores/') or path.startswith('/api/leaderboard/'):
            return 'rank-service'
        
        # Tournaments → tournament-service (8003)
        elif path.startswith('/api/tournaments/') or path.startswith('/api/tournament-teams/') or path.startswith('/api/tournament-rounds/'):
            return 'tournament-service'
        
        # Health check
        elif path.startswith('/api/health/'):
            return 'user-service'  # Or any service

        return None

    def get_target_path(self, request):
        """Формирование пути для целевого сервиса"""

        path = request.path
        if path.startswith('/api/'):
            return path  # Оставляем как есть
        return path

    def proxy_request(self, request, target_url):
        """Проксирование HTTP запроса"""
        try:

            headers = {}


            important_headers = [
                'Authorization', 'Content-Type', 'Accept', 'User-Agent',
                'Accept-Language', 'Accept-Encoding'
            ]

            for header_name in important_headers:
                header_value = request.headers.get(header_name)
                if header_value:
                    headers[header_name] = header_value

            # Логируем заголовки для отладки
            logger.info(f"Forwarding headers: {headers}")

            # Подготавливаем данные
            data = None
            json_data = None

            if request.method in ['POST', 'PUT', 'PATCH']:
                content_type = request.headers.get('Content-Type', '')

                if 'application/json' in content_type:
                    try:
                        if request.body:
                            json_data = json.loads(request.body.decode('utf-8'))
                            logger.info(f"JSON data: {json_data}")
                    except (json.JSONDecodeError, UnicodeDecodeError) as e:
                        logger.error(f"Failed to parse JSON: {e}")
                        data = request.body
                else:
                    data = request.body


            params = dict(request.GET.items())
            if params:
                logger.info(f"Query params: {params}")

            response = requests.request(
                method=request.method,
                url=target_url,
                headers=headers,
                json=json_data,
                data=data if json_data is None else None,
                params=params,
                timeout=30
            )

            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response content: {response.text[:200]}...")  # Логируем первые 200 символов


            django_response = HttpResponse(
                response.content,
                status=response.status_code,
                content_type=response.headers.get('content-type', 'application/json')
            )


            response_headers_to_copy = ['Content-Type', 'Cache-Control', 'ETag']
            for key in response_headers_to_copy:
                if key in response.headers:
                    django_response[key] = response.headers[key]

            return django_response

        except requests.exceptions.Timeout:
            logger.error(f"Timeout when calling {target_url}")
            return JsonResponse({'error': 'Service timeout'}, status=504)
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error when calling {target_url}: {e}")
            return JsonResponse({'error': 'Service unavailable'}, status=503)
        except Exception as e:
            logger.error(f"Error proxying request to {target_url}: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)


proxy_view = ProxyView.as_view()
