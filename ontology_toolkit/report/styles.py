def get_styles():

    return """
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    max-width: 1100px;
    margin: 40px auto;
    padding: 0 24px;
    background: #fbfaf7;
    color: #4f5b66;
    line-height: 1.6;
}

h1,
h2,
h3 {
    color: #2f3b45;
    font-weight: 600;
}

h1 {
    margin-bottom: 0.25em;
}

h2 {
    margin-top: 2em;
    padding-bottom: 0.35em;
    border-bottom: 1px solid #e8e3dc;
    color:#b31b1b;
}

p {
    color: #55616c;
}

a {
    color: #5f7ea8;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

/* Summary cards */

.cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;
    margin: 30px 0;
}

.card {
    background: #ffffff;
    border: 1px solid #e8e3dc;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}

.label {
    color: #7b848d;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.value {
    font-size: 2.4rem;
    font-weight: 700;
    color: #2f3b45;
    margin-top: 8px;
}

/* Tables */

table {
    width: 100%;
    border-collapse: collapse;
    margin: 18px 0 30px;
    background: #ffffff;
    border: 1px solid #e8e3dc;
}

th,
td {
    padding: 10px 14px;
    text-align: left;
}

th {
    background: #f4f1eb;
    color: #2f3b45;
    font-weight: 600;
    border-bottom: 1px solid #e8e3dc;
}

td {
    border-bottom: 1px solid #f0ece6;
}

tbody tr:nth-child(even) {
    background: #fcfbf9;
}

/* Code / Turtle */

pre,
.rdf-viewer {
    background: #f6f5f2;
    border: 1px solid #e5dfd7;
    border-left: 5px solid #5f7ea8;
    border-radius: 8px;
    padding: 20px;
    overflow: auto;
    max-height: 700px;

    font-family:
        "SF Mono",
        "IBM Plex Mono",
        Menlo,
        Consolas,
        monospace;

    font-size: 13px;
    line-height: 1.6;
    color: #3f4448;
    white-space: pre;
}

/* Inline code */

code {
    font-family:
        "SF Mono",
        "IBM Plex Mono",
        Menlo,
        Consolas,
        monospace;
}

/* Horizontal rule */

hr {
    border: none;
    border-top: 1px solid #e8e3dc;
    margin: 40px 0;
}

/* Report Header */

.report-header {
    margin-bottom: 24px;
}

/* Sticky navigation */

.toc {
    position: sticky;
    top: 0;
    z-index: 1000;
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin: 30px 0 40px;
    padding: 18px;
    background: rgba(248,246,242,.96);
    backdrop-filter: blur(10px);
    border: 1px solid #e8e3dc;
    border-radius: 12px;
    transition:
        padding .25s ease,
        box-shadow .25s ease,
        border-radius .25s ease,
        gap .25s ease;
}

.toc a {
    display: inline-flex;
    align-items: center;
    padding: 8px 14px;
    border-radius: 999px;
    color: #4f5b66;
    text-decoration: none;
    font-size: .95rem;
    font-weight: 500;
    transition: all .2s ease;
}

.toc a:hover {
    background: #5f7ea8;
    color: white;
}

/* Compact sticky version */

.toc.compact {
    padding: 8px 14px;
    gap: 8px;
    border-radius: 0 0 12px 12px;
    box-shadow: 0 6px 18px rgba(0,0,0,.08);
}

.toc.compact a {
    padding: 5px 12px;
    font-size: .88rem;
}
html {
    scroll-behavior: smooth;
    scroll-padding-top: 50px;
}

h2[id] {
    scroll-margin-top: 50px;
}

[id] {
    scroll-margin-top: 50px;
}

"""