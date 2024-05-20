import subprocess
import re
import json


class Website:
    def __init__(self, data):
        self.name = data["name"]
        self.url = data["url"]
        self.score = int(data["score"] * 100)
        self.performance = int(data["detail"]["performance"] * 100)
        self.accessibility = int(data["detail"]["accessibility"] * 100)
        self.best_practices = int(data["detail"]["best-practices"] * 100)
        self.seo = int(data["detail"]["seo"] * 100)
        self.pwa = int(data["detail"]["pwa"] * 100)

    def __str__(self):
        return f"""name: {self.name}
url: {self.url}
score: {self.score}
performance: {self.performance}
accessibility: {self.accessibility}
best practices: {self.best_practices}
seo: {self.seo}
pwa: {self.pwa}"""


try:
    open("audits.txt", "w").close()
except FileNotFoundError:
    open("audits.txt", "x")

with open("urls.txt") as file:
    urls = [re.sub("\n", "", i) for i in file.readlines()]

for url in urls:
    subprocess.run(["powershell", "-Command", f"npx lighthouse-batch -s {url}"], capture_output=True)
    site = Website(json.loads(open("report\\lighthouse\\summary.json").read()[1:-1]))
    with open("audits.txt", "a") as file:
        file.write(f"{str(site)}\n\n")
