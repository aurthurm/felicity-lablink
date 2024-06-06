from flablink.felicity.factory import create_app

config = dict()
config["title"] = "Felicity LabLink"
config["description"] = "Serial and Socket Communication Gateway"

app = create_app(config)
