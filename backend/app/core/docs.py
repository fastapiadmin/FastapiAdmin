from typing import Annotated

from starlette.responses import HTMLResponse
from typing_extensions import Doc


def get_custom_ui_html(
    *,
    openapi_url: Annotated[
        str,
        Doc(
            """
            The OpenAPI URL that Swagger UI should load and use.

            This is normally done automatically by FastAPI using the default URL
            `/openapi.json`.
            """
        ),
    ],
    title: Annotated[
        str,
        Doc(
            """
            The HTML `<title>` content, normally shown in the browser tab.
            """
        ),
    ],
    swagger_js_url: Annotated[
        str,
        Doc(
            """
            The URL to use to load the Swagger UI JavaScript.

            It is normally set to a CDN URL.
            """
        ),
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
    swagger_css_url: Annotated[
        str,
        Doc(
            """
            The URL to use to load the Swagger UI CSS.

            It is normally set to a CDN URL.
            """
        ),
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    swagger_favicon_url: Annotated[
        str,
        Doc(
            """
            The URL of the favicon to use. It is normally shown in the browser tab.
            """
        ),
    ] = "https://fastapi.tiangolo.com/img/favicon.png",
) -> HTMLResponse:
    """
    Generate and return the HTML  that loads Swagger UI for the interactive
    API docs (normally served at `/docs`).

    You would only call this function yourself if you needed to override some parts,
    for example the URLs to use to load Swagger UI's JavaScript and CSS.

    Read more about it in the
    [FastAPI docs for Configure Swagger UI](https://fastapi.tiangolo.com/how-to/configure-swagger-ui/)
    and the [FastAPI docs for Custom Docs UI Static Assets (Self-Hosting)](https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/).
    """
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link type="text/css" rel="stylesheet" href="{swagger_css_url}">
    <link rel="shortcut icon" href="{swagger_favicon_url}">
    <title>{title}</title>
    </head>
    <body>
    <div id="swagger-ui"></div>
    <script src="{swagger_js_url}"></script>
    <script>
        ui.configure({{url: '{openapi_url}'}});
        ui.initialize();
    </script>
    </body>
    </html>
    """
    return HTMLResponse(html)
