def render_relationship_types(schema):

    html = "<h2>Relationship Types</h2>"
    html += '<div class="cards">'

    for relationship in sorted(
        schema.relationship_types.values(),
        key=lambda r: r.name,
    ):

        html += f"""
<div class="card">

<h3>{relationship.name}</h3>

<p><strong>Instances:</strong> {relationship.count}</p>

<p>
<strong>Source:</strong>
{", ".join(sorted(relationship.source_labels))}
</p>

<p>
<strong>Target:</strong>
{", ".join(sorted(relationship.target_labels))}
</p>

<table>

<tr>
<th>Property</th>
<th>Type</th>
</tr>
"""

        for prop in sorted(
            relationship.properties.values(),
            key=lambda p: p.name,
        ):

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