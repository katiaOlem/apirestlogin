from operator import index
import web

urls = (
    '/', 'index',
    "/user/(.*)", "login",
    '/validate/', 'Validate',
)
app = web.application(urls, globals())
render = web.template.render("templates/")

class index:
    def GET(self):
        return render.index()

class login:
    def GET(self):
        return render.login()

           
if __name__ == "__main__":
    app.run()