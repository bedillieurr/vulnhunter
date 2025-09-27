import json, os, logging
from jinja2 import Template

LOG = logging.getLogger("vulnhunter.reporting.reporter")

HTML_TMPL = """
<!doctype html>
<html>
<head><meta charset="utf-8"><title>VulnHunter Report - {{ target }}</title></head>
<body>
<h1>VulnHunter Report — {{ target }}</h1>
<p>Total findings (scored): {{ findings|length }}</p>
<ol>
{% for f in findings %}
  <li><b>{{ f.host }}</b> — score: {{ f.score }} — tags: {{ f.tags|join(', ') }}</li>
{% endfor %}
</ol>
</body>
</html>
"""

class Reporter:
    def __init__(self, result):
        self.result = result

    def to_json(self, path):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w") as fh:
            json.dump(self.result, fh, indent=2)
        LOG.info("Saved JSON report to %s", path)
        return path

    def to_html(self, path):
        t = Template(HTML_TMPL)
        html = t.render(target=self.result.get("target"), findings=self.result.get("scored", []))
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w") as fh:
            fh.write(html)
        LOG.info("Saved HTML report to %s", path)
        return path
