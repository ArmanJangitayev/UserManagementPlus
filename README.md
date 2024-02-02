# Аутентификацией и Авторизацией пользователей.
### class LoginPageView(View):
Реализовал аутентификацию во views.py, где в дальнейшем свявал с auth.py, в которой использовал логику кастомного решения.
    

    


### class RegisterPageView(View):
Реализована регистрация юзера, где мы использовал в логике auth.py
    template_name = 'auth/registration_page.html'
    form_class = forms.UserRegForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        message = ''
        print(form.data)
        user_id = None

        response = render(request, self.template_name, context={'form': form, 'message': message})

        if form.is_valid():
            user = AuthSystem.register_user(
                request,
                **form.cleaned_data,
            )
            user_id = user.id
            if user is not None:
                response = redirect('home_page')
                CookieManager.set_cookie_expiration(response, 'user_id', user_id, expiration_minutes=360)

            else:
                message = 'Registration failed!'
        return response
### Связал CookieManager с регистрацией где, при регистрации, cookie появляется с условием авторизацией.
    def logout(request):
    AuthSystem.logout_user(request)

    response = redirect('home_page')
    CookieManager.delete_cookie(response, 'logged_in')
    return response

## Реализовал функцию SQLDBManager для связи с базой данных.
def users_all(request):
db_manager = SQLDBManager()
db_manager.connect_to_db()
### class SQLDBManager:
    def connect_to_db(self):
        # Метод для установки соединения с базой данных
        return connection

    def execute_query(self, query, params=None):
        con = self.connect_to_db()
        # Метод для выполнения SQL-запроса
        with con.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()  # Получение результатов запроса, если они есть
        return result

    query = "SELECT id, username, email FROM authorization_user"
    params = ['arman']
    result = db_manager.execute_query(query, params)

   
    for row in result:
        print(row)

    return render(request, 'auth/users.html', {"table": result})

### Реализация api для связи с другими сервисами, связал освновную логику в serializers.py
### class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

# Реализация SessionMaganer
### class SessionManager:
    @staticmethod
    def create_session(request, user=None):
        request.session['username'] = user.username
        request.session['email'] = user.email
        request.session['name'] = user.name
# Здесь прописана дальнейшая логика  session 
    @staticmethod
    def destroy_session(request):
        if 'username' in request.session:
            del request.session['username']
        if 'email' in request.session:
            del request.session['email']
        if 'name' in request.session:
            del request.session['name']


Так же запустил docker-container для базы данных PostgreSql
## Files 
    def handle_uploaded_file(f, filename):
    if filename.endswith('.jpg'):
        print('compressing image')
        f = compress_image(f)
    with open("media/files/" + filename, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


    def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"], form.cleaned_data['title'])
            return redirect('home_page')

    else:
        form = UploadFileForm()
    return render(request, "files.html", {"form": form})
Реализовал отправку и сжатие файла во views.py, дальнейшие дествия преобразования сжатия вывел во helpers.py
