import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from pages import page1, page2

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    """Displays the page that corresponds to the given pathname.

    :param pathname: The current pathname (the last part of the URL) of the page.
    :return: The page that should be at that pathname; otherwise a 404 page.
    """
    if pathname == '/page1':
        return page1.layout
    elif pathname == '/page2':
        return page2.layout
    else:
        return '404'  # TODO: Make special 404 page


if __name__ == '__main__':
    app.run_server(debug=True)
