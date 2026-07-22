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

<script>
document.addEventListener("DOMContentLoaded", () => {{

    const nav = document.querySelector(".toc");

    if (!nav) return;

    const stickyPoint = nav.offsetTop;

    let compact = false;

    window.addEventListener("scroll", () => {{

        const shouldCompact = window.scrollY > stickyPoint;

        if (shouldCompact !== compact) {{
            compact = shouldCompact;
            nav.classList.toggle("compact", compact);
        }}

    }});

}});
</script>

</body>

</html>
"""