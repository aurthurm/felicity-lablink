from flablink.felicity.factory import create_app

config = dict()
config["title"] = "ASTM Results Dashboard"

app = create_app(config)