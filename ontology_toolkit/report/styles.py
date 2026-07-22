def get_styles():

    return """
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    max-width: 1100px;
    margin: 40px auto;
    padding: 0 24px;
    background: #fafafa;
    color: #222;
}

.cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;
    margin-top: 30px;
}

.card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 2px 8px rgba(0,0,0,.04);
}

.label {
    color: #666;
    font-size: .9rem;
    text-transform: uppercase;
    letter-spacing: .08em;
}

.value {
    font-size: 2.5rem;
    font-weight: 700;
    margin-top: 8px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 12px;
}

th {
    text-align: left;
    border-bottom: 1px solid #ddd;
    padding: 8px 0;
}

td {
    padding: 6px 0;
    border-bottom: 1px solid #f2f2f2;
}

h3 {
    margin-top: 0;
}

pre {
    background: #f7f7f7;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 20px;
    overflow-x: auto;
    line-height: 1.6;
    font-family: SFMono-Regular, Menlo, Consolas, monospace;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 30px;
}

th,
td {
    padding: 10px 12px;
    border: 1px solid #e5e7eb;
    text-align: left;
}

th {
    background: #f3f4f6;
    font-weight: 600;
}

tbody tr:nth-child(even) {
    background: #fafafa;
}

"""