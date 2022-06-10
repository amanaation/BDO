import jinja2
import os

class Plotting:

    def plot(self, merchant_id, data):
        templateLoader = jinja2.FileSystemLoader(searchpath="")
        templateEnv = jinja2.Environment(loader=templateLoader)
        path = os.path.dirname(os.path.realpath(__file__))
        TEMPLATE_FILE = f"templates/index.html"
        template = templateEnv.get_template(TEMPLATE_FILE)
        outputText = template.render(data=data)  # this is where to put args to the template renderer

        if not os.path.exists("output/"):
            os.mkdir("output")

        with open(f"output/{merchant_id}.html", "w") as file:
            file.write(outputText)
