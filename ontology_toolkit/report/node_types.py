def render_node_types(schema):

    html = "<h2>Node Types</h2>"
    html += '<div class="cards">'

    for node in sorted(schema.node_types.values(), key=lambda n: n.label):

        html += f"""
<div class="card">

<h3>{node.label}</h3>

<p><strong>Instances:</strong> {node.count}</p>

<table>

<tr>
<th>Property</th>
<th>Type</th>
</tr>
"""

        for prop in sorted(node.properties.values(), key=lambda p: p.name):

            html += f"""
<tr>
<td>{prop.name}</td>
<td>{prop.data_type}</td>
</tr>
"""

        html += """
</table>

</div>
"""

    html += "</div>"

    return html