def get_styles():

    return """
/* ==========================================================================
   Base Layout
   ========================================================================== */

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    max-width: 1400px;
    margin: 40px auto;
    padding: 0 20px;
    background: #fbfaf7;
    color: #4f5b66;
    line-height: 1.6;
}

html {
    scroll-behavior: smooth;
    scroll-padding-top: 50px;
}

.report-text {
    max-width: 75ch;
}


/* ==========================================================================
   Typography
   ========================================================================== */

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
    color: #b31b1b;
}

h3 {
    display: flex;
    align-items: baseline;
    gap: 12px;
    margin: 28px 0 8px;
}

.viewer-filename {
    font-size: .78rem;
    font-weight: 400;
    color: #555;
    font-family:
        "SF Mono",
        Menlo,
        Consolas,
        monospace;
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


/* ==========================================================================
   Summary Cards
   ========================================================================== */

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

.viewer-content .card {
    padding: 16px;
    margin-bottom: 24px;
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

.overview-meta {
    margin-top: 1.25rem;
    color: #666;
    font-size: 0.95rem;
}


/* ==========================================================================
   Tables
   ========================================================================== */

table {
    width: 100%;
    table-layout: fixed;
    border-collapse: collapse;
    margin: 18px 0 30px;
    background: #ffffff;
    border: 1px solid #e8e3dc;
}

th,
td {
    padding: 10px 14px;
    text-align: left;
    overflow-wrap: anywhere;
    word-break: break-word;
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


/* ==========================================================================
   RDF / Turtle Viewer
   ========================================================================== */

.rdf-viewer {
    border: 1px solid #e5dfd7;
    border-left: 3px solid #5f7ea8;
    border-radius: 8px;
    overflow: auto;
    max-height: 900px;
}

.viewer-content pre[class*="language-"] {
    margin: 0 !important;
    padding: 10px 12px !important;
}

.viewer-content pre[class*="language-"],
.viewer-content code[class*="language-"] {
    font-size: .80rem !important;
    line-height: 1.4 !important;
}

code {
    font-family:
        "SF Mono",
        "IBM Plex Mono",
        Menlo,
        Consolas,
        monospace;
}


/* ==========================================================================
   Report Structure
   ========================================================================== */

hr {
    border: none;
    border-top: 1px solid #e8e3dc;
    margin: 40px 0;
}

.report-header {
    margin-bottom: 24px;
}

.report-footer {
    margin-top: 80px;
    padding-bottom: 40px;
    color: #7b848d;
    font-size: .9rem;
    text-align: center;
}

.report-footer a {
    color: #5f7ea8;
}


/* ==========================================================================
   Sticky Top Navigation
   ========================================================================== */

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

h2[id],
h3[id],
[id] {
    scroll-margin-top: 60px;
}


/* ==========================================================================
   Viewer Layout
   ========================================================================== */

.viewer-layout {
    display: grid;
    grid-template-columns: 160px minmax(0, 1fr);
    gap: 20px;
    align-items: start;
    margin-top: 24px;
}

.viewer-content {
    min-width: 0;
}

.viewer-nav {
    position: sticky;
    top: var(--viewer-nav-top, 80px);
    display: flex;
    flex-direction: column;
    gap: 6px;
    padding: 12px;
    background: #f8f6f2;
    border: 1px solid #e8e3dc;
    border-radius: 12px;
}

.viewer-nav a {
    display: block;
    padding: 8px 10px;
    border-radius: 8px;
    color: #4f5b66;
    text-decoration: none;
    font-size: .88rem;
    font-weight: 500;
    transition: all .2s ease;
}

.viewer-nav a:hover {
    background: #5f7ea8;
    color: white;
}


/* ==========================================================================
   Responsive
   ========================================================================== */

@media (max-width: 900px) {

    .report-text {
        max-width: none;
    }

    .viewer-layout {
        grid-template-columns: 1fr;
    }

    .viewer-nav {
        position: static;
        flex-direction: row;
        flex-wrap: wrap;
        margin-bottom: 24px;
    }

    h3 {
        flex-wrap: wrap;
    }

}
"""