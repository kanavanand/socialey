import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

def prepeare_Dashboard_content():
    PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
    app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
    # make a reuseable navitem for the different examples
    nav_item = dbc.NavItem(dbc.NavLink("Link", href="#"))
    # make a reuseable dropdown for the different examples
    # this example has a search bar and button instead of navitems / dropdowns
    search_navbar = dbc.Navbar(
        dbc.Container(
            [
                dbc.NavbarBrand("Search", href="#"),
                dbc.NavbarToggler(id="navbar-toggler3"),
                dbc.Collapse(
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Input(type="search", placeholder="Search")
                            ),
                            dbc.Col(
                                dbc.Button(
                                    "Search", color="primary", className="ml-2"
                                ),
                                # set width of button column to auto to allow
                                # search box to take up remaining space.
                                width="auto",
                            ),
                        ],
                        no_gutters=True,
                        className="ml-auto flex-nowrap mt-3 mt-md-0",
                        align="center",
                    ),
                    id="navbar-collapse3",
                    navbar=True,
                ),
            ]
        ),
        className="mb-5",
    )

    # custom navbar based on https://getbootstrap.com/docs/4.1/examples/dashboard/
    dashboard = dbc.Navbar(
        [
            dbc.Col(dbc.NavbarBrand("Dashboard", href="/"), sm=3, md=2),
            dbc.Col(dbc.Input(type="search", placeholder="Search here")),
            dbc.Col(
                dbc.Nav(dbc.NavItem(dbc.NavLink("All Sources")), navbar=True),
                width="auto",
            ),
            dbc.Col(
            dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Overall", header=True),
                dbc.DropdownMenuItem("Twitter", href="#"),
                dbc.DropdownMenuItem("Facebook", href="#"),
                dbc.DropdownMenuItem("Instagram", href="#"),
                dbc.DropdownMenuItem("Blogs", href="#")
            ]),width="auto",)
        ],
        color="dark",
        dark=True,
    )
    return dashboard