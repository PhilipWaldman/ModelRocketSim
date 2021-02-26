import dash_html_components as html


def get_layout():
    return html.Div([
        html.H3('Plots')
    ],
        style={
            'margin-left': '2rem',
            'margin-right': '2rem'
        }
    )
