class HelloMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        ignored_paths = ['/login/', '/register/']
        if request.path in ignored_paths:
            return self.get_response(request)


        print("Hello Middleware")
        print(request)
        response = self.get_response(request)
        return response