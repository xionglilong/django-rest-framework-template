from django.utils.deprecation import MiddlewareMixin


class CorsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Expose-Headers"] = "*"
        response["Access-Control-Allow-Methods"] = "*"
        # response["Access-Control-Max-Age"] = "*"
        return response
