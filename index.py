import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from pages import page1, page2, page404, home_page

all_pages = {
    '/page1': 'Page 1',
    '/page2': 'Page 2'
}

# themes = {'Cerulean': dbc.themes.CERULEAN, 'Cosmo': dbc.themes.COSMO, 'Cyborg': dbc.themes.CYBORG,
#          'Darkly': dbc.themes.DARKLY, 'Flatly': dbc.themes.FLATLY, 'Journal': dbc.themes.JOURNAL,
#          'Litera': dbc.themes.LITERA, 'Lumen': dbc.themes.LUMEN, 'Lux': dbc.themes.LUX, 'Materia': dbc.themes.MATERIA,
#          'Minty': dbc.themes.MINTY, 'Pulse': dbc.themes.PULSE, 'Sandstone': dbc.themes.SANDSTONE,
#          'Simplex': dbc.themes.SIMPLEX, 'Sketchy': dbc.themes.SKETCHY, 'Slate': dbc.themes.SLATE,
#          'Solar': dbc.themes.SOLAR, 'Spacelab': dbc.themes.SPACELAB, 'Superhero': dbc.themes.SUPERHERO,
#          'United': dbc.themes.UNITED, 'Yeti': dbc.themes.YETI}

navbar = dbc.NavbarSimple(
    children=[
        # All pages dropdown
        dbc.DropdownMenu(
            children=[dbc.DropdownMenuItem(all_pages[page], href=page) for page in all_pages],
            nav=True,
            in_navbar=True,
            label='Pages'
        ),
        # TODO: Theme selector dropdown
        # dbc.DropdownMenu(
        #     children=[dbc.DropdownMenuItem(theme) for theme in themes],
        #     nav=True,
        #     in_navbar=True,
        #     label='Theme',
        #     id='theme-dropdown'
        # )
    ],
    brand='WARP',
    brand_href='/'
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'))
def display_page(pathname):
    """Displays the page that corresponds to the given pathname.

    :param pathname: The current pathname (the last part of the URL) of the page.
    :return: The page that should be at that pathname; otherwise a 404 page.
    """
    if pathname == '/':
        return home_page.layout
    elif pathname == '/page1':
        return page1.layout
    elif pathname == '/page2':
        return page2.layout
    else:
        return page404.layout


if __name__ == '__main__':
    app.run_server(debug=True)
