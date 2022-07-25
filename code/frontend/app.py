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

class getclientes:
    def GET(self):
        return render.get_clientes()

           
if __name__ == "__main__":
    app.run()