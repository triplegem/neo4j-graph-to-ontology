"""
Schema summary section for the HTML report.
"""


def render_schema_summary(schema):
    """Render a summary of the discovered graph schema."""

    html = """
<h2 id="schema-summary">Schema Summary</h2>

<p>
The discovered schema contains the following node and relationship
types. Detailed information for each type is provided later in this
report.
</p>

<h3>Node Types</h3>

<table>
<thead>
<tr>
    <th>Label</th>
    <th>Instances</th>
    <th>Properties</th>
</tr>
</thead>
<tbody>
"""

    # Node types
    for node in sorted(schema.node_types.values(), key=lambda n: n.label):

        html += f"""
<tr>
    <td>{node.label}</td>
    <td>{node.count}</td>
    <td>{len(node.properties)}</td>
</tr>
"""

    html += """
</tbody>
</table>

<h3>Relationship Types</h3>

<table>
<thead>
<tr>
    <th>Relationship</th>
    <th>Instances</th>
    <th>Properties</th>
</tr>
</thead>
<tbody>
"""

    # Relationship types
    for relationship in sorted(
        schema.relationship_types.values(),
        key=lambda r: r.name,
    ):

        html += f"""
<tr>
    <td>{relationship.name}</td>
    <td>{relationship.count}</td>
    <td>{len(relationship.properties)}</td>
</tr>
"""

    html += """
</tbody>
</table>
"""

    return html