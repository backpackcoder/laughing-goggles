import tornado.ioloop
import tornado.template
import tornado.web

from map_tools import merge_tiles

loader = tornado.template.Loader("./web")
port = 8888
settings = {"debug": True,
            "compiled_template_cache": False,
            "autoreload": True,
            "static_path": "./node_modules/leaflet/dist"}


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(loader.load("at-map.html").generate())


def make_app():
    handlers = [(r'/tiles/(.*)',
                 tornado.web.StaticFileHandler,
                 {'path': './tiles'}),
                (r"/", MainHandler)]
    return tornado.web.Application(handlers, **settings)


if __name__ == "__main__":
    merge_tiles.merge(["tiles/Test-Layer-1",
                       "tiles/Test-Layer-2"],
                      "tiles/output")
    app = make_app()
    app.listen(port)
    print "webapp started at http://localhost:{}".format(port)
    tornado.ioloop.IOLoop.current().start()
