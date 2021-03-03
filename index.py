import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from pages import thrust_curve_page, page404, home_page, plots_page
from pages.rocket_builder import rocket_builder_page

all_pages = {
    '/thrust_curves': 'Thrust curves',
    '/rocket_builder': 'Rocket builder',
    '/plots': 'Plots'
}

navbar = dbc.NavbarSimple(
    children=[
        # All pages dropdown
        dbc.DropdownMenu(
            children=[dbc.DropdownMenuItem(all_pages[page], href=page) for page in all_pages],
            nav=True,
            in_navbar=True,
            label='Pages'
        )
    ],
    brand='WARP',
    brand_href='/'
)

app.layout = html.Div([
    dcc.Store(id='thrust-curve-data', storage_type='session'),
    dcc.Store(id='rocket-builder-data', storage_type='session'),
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'),
    State('thrust-curve-data', 'data'),
    State('rocket-builder-data', 'data'))
def display_page(pathname, thrust_curve_data, rocket_builder_data):
    """Displays the page that corresponds to the given pathname.

    :param pathname: The current pathname (the last part of the URL) of the page.
    :param thrust_curve_data:
    :param rocket_builder_data:
    :return: The page that should be at that pathname; otherwise a 404 page.
    """
    if pathname == '/':
        return home_page.layout
    elif pathname == thrust_curve_page.pathname:
        return thrust_curve_page.get_layout(thrust_curve_data)
    elif pathname.startswith(rocket_builder_page.pathname):
        return rocket_builder_page.get_layout(rocket_builder_data)
    elif pathname == plots_page.pathname:
        return plots_page.get_layout()
    else:
        return page404.layout


if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server(debug=False, port=8080, host='0.0.0.0')  # Run on LAN (replace host with your IP address)
