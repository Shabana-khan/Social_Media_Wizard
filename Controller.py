import os
import web

web.config.debug = False  # Disable debugging

from Models import RegisterModel, LoginModel, Posts

urls = (
    '/', 'Home',
    '/register', 'Register',
    '/login', 'Login',
    '/logout', 'Logout',
    '/postregistration', 'PostRegistration',
    '/check-login', 'CheckLogin',
    '/post-activity', 'PostActivity',
    '/messages/(.*)','Messages',
    '/profile/(.*)/activity', 'Messages',
    '/profile/(.*)/info', 'Info',
    '/profile/(.*)/code', 'Code',
    '/settings/(.*)', 'Info',
    '/profile/(.*)','Messages',
    '/update-settings','UpdateSettings',
    '/submit-comment', 'SubmitComment',
    '/upload-image/(.*)', 'UploadImage'
)
app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore("sessions"), initializer={'user' : None})
session_data = session._initializer

base_render = web.template.render('Views/Templates/', globals={'session':session_data, 'current_user':session_data["user"]})
render = web.template.render("Views/Templates", base="MainLayout", globals={'session':session_data, 'current_user':session_data["user"]})
home_render = web.template.render("Views/Templates", base="Home", globals={'session':session_data, 'current_user':session_data["user"]})

class Home:
    def GET(self):
        login = LoginModel.LoginModel()

        if session_data["user"] is not None:
            post_model = Posts.Posts()
            posts = post_model.get_all_posts()
            home_page = base_render.Messages(posts)
        else:
            home_page = "<h1>Welcome CodeWizard</h1>"
        return render.Home(home_page)


class Messages:
    def GET(self, user):
        login = LoginModel.LoginModel()
        user_info = login.get_profile(user)
        if "about" not in user_info:
            user_info["about"]="None"
        if "hobbies" not in user_info:
            user_info["hobbies"] = "None"
        if "birthday" not in user_info:
            user_info["birthday"] = "None"
        if "avatar" not in user_info:
            user_info["avatar"] = "None"
        if "background" not in user_info:
            user_info["background"] = "None"
        post_model = Posts.Posts()
        posts = post_model.get_user_posts(user)
        if(web.ctx.path == "/profile/"+user+"/activity" or web.ctx.path == "/profile/"+user):
            if(web.ctx.path == "/profile/"+user):
                session_data["user"] = user_info
            message_page = base_render.Messages(posts)
            profile_page = home_render.Profile(message_page, False, user_info)
            return render._base(profile_page)
        elif(web.ctx.path == "/messages/"+user):
            message_page = base_render.Messages(posts)
            return render.Home(message_page)


class Info:
    def GET(self, user):
        info_form = False
        login = LoginModel.LoginModel()
        user_info = login.get_profile(user)
        if "about" not in user_info:
            user_info["about"]="None"
        if "hobbies" not in user_info:
            user_info["hobbies"] = "None"
        if "birthday" not in user_info:
            user_info["birthday"] = "None"
        if "avatar" not in user_info:
            user_info["avatar"] = "None"
        if "background" not in user_info:
            user_info["background"] = "None"
        if(web.ctx.path == "/settings/"+user):
            info_form = True
        info_page = base_render.Info(info_form, user_info)
        profile_page = home_render.Profile(info_page, info_form, user_info)
        return render._base(profile_page)

class Code:
    def GET(self, user):
        login = LoginModel.LoginModel()
        user_info = login.get_profile(user)
        if "avatar" not in user_info:
            user_info["avatar"] = "None"
        if "background" not in user_info:
            user_info["background"] = "None"
        code_page = base_render.Code()
        profile_page = home_render.Profile(code_page, False, user_info)
        return render._base(profile_page)

class Register:
    def GET(self):
        return render.Register()

class Login:
    def GET(self):
        return render.Login()

class PostRegistration:
    def POST(self):
        data = web.input()

        reg_model = RegisterModel.RegisterModel()
        reg_model.insert_user(data)
        return data.username

class CheckLogin:
    def POST(self):
        data = web.input()
        login = LoginModel.LoginModel()
        isCorrect = login.check_user(data)

        if isCorrect:
            session_data["user"] = isCorrect
            return isCorrect

        return "error"

class PostActivity:
    def POST(self):
        data = web.input()
        data.username = session_data['user']['username']
        post_model = Posts.Posts()
        return post_model.insert_post(data)

class UpdateSettings:
    def POST(self):
        data = web.input()
        data.username = session_data["user"]["username"]
        print(data)
        settings_model = LoginModel.LoginModel()
        if settings_model.update_info(data):
            return "success"
        else:
            return "A fatal error has occurred"


class Logout:
    def GET(self):
        session["user"] = None
        session_data["user"] = None
        session.kill()
        return "success"

class SubmitComment:
    def POST(self):
        data = web.input()
        data.username = session_data["user"]["username"]

        post_model = Posts.Posts()
        added_comment =post_model.add_comment(data)

        if added_comment:
            return added_comment
        else:
            return {"error": "403"}

class UploadImage:
    def POST(self, type):
        file = web.input(avatar={}, background={})
        file_dir = os.getcwd() + "/static/images/" + session_data["user"]["username"]

        if not os.path.exists(file_dir):
            os.mkdir(file_dir)

        if "avatar" or "background" in file:
            filepath = file[type].filename.replace('\\', '/')
            filename = filepath.split("/")[-1]
            f = open(file_dir + "/" + filename, 'wb')
            f.write(file[type].file.read())
            f.close()

            update = {}
            update["type"] = type
            update["img"] = '/static/images/' + session_data["user"]["username"] + "/" + filename
            update["username"] = session_data["user"]["username"]

            account_model = LoginModel.LoginModel()
            update_avatar = account_model.update_image(update)
            print(update_avatar)

        raise web.seeother("/settings/"+session_data["user"]["username"])


if __name__ == "__main__":
    app.run()