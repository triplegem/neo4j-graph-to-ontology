from ontology_toolkit.report.styles import get_styles


def render_page(title, body):

    return f"""<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="utf-8">

<title>{title}</title>

<style>

{get_styles()}

</style>

</head>

<body>

{body}

</body>

</html>
"""