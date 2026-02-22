"""
FastAPI class and main application.
"""
import inspect
import logging
from typing import Any, Callable, Coroutine, Dict, List, Optional, Sequence, Type, Union

from fastapi import routing
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute


logger = logging.getLogger(__name__)


class FastAPI:
    """
    The main FastAPI class.
    """

    def __init__(
        self,
        *,
        debug: bool = False,
        routes: Optional[List[routing.BaseRoute]] = None,
        title: str = "FastAPI",
        description: str = "",
        version: str = "0.1.0",
        openapi_url: Optional[str] = "/openapi.json",
        openapi_tags: Optional[List[Dict[str, Any]]] = None,
        servers: Optional[List[Dict[str, Union[str, Any]]]] = None,
        docs_url: Optional[str] = "/docs",
        redoc_url: Optional[str] = "/redoc",
        swagger_ui_oauth2_redirect_url: Optional[str] = "/docs/oauth2-redirect",
        swagger_ui_init_oauth: Optional[Dict[str, Any]] = None,
        middleware: Optional[Sequence[Middleware]] = None,
        exception_handlers: Optional[Dict[Union[int, Type[Exception]], Callable]] = None,
        on_startup: Optional[Sequence[Callable[[], Any]]] = None,
        on_shutdown: Optional[Sequence[Callable[[], Any]]] = None,
        default_response_class: Type[routing.Response] = routing.JSONResponse,
        dependencies: Optional[Sequence[routing.Depends]] = None,
        openapi_prefix: str = "",
    ) -> None:
        self.debug = debug
        self.routes: List[routing.BaseRoute] = routes or []
        self.title = title
        self.description = description
        self.version = version
        self.openapi_url = openapi_url
        self.openapi_tags = openapi_tags
        self.servers = servers
        self.docs_url = docs_url
        self.redoc_url = redoc_url
        self.swagger_ui_oauth2_redirect_url = swagger_ui_oauth2_redirect_url
        self.swagger_ui_init_oauth = swagger_ui_init_oauth
        self.middleware = middleware or []
        self.exception_handlers = exception_handlers or {}
        self.on_startup = on_startup or []
        self.on_shutdown = on_shutdown or []
        self.default_response_class = default_response_class
        self.dependencies = dependencies or []
        self.openapi_prefix = openapi_prefix
        self.openapi_schema: Optional[Dict[str, Any]] = None
        self._openapi_schema_cache: Optional[Dict[str, Any]] = None

    def add_middleware(
        self,
        middleware_class: Type,
        **options: Any,
    ) -> None:
        self.middleware.append(Middleware(middleware_class, **options))

    def add_route(
        self,
        path: str,
        route: routing.BaseRoute,
    ) -> None:
        self.routes.append(route)

    def include_router(
        self,
        router: routing.APIRouter,
        *,
        prefix: str = "",
        tags: Optional[List[str]] = None,
        dependencies: Optional[Sequence[routing.Depends]] = None,
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        default_response_class: Optional[Type[routing.Response]] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        include_in_schema: bool = True,
    ) -> None:
        self.routes.extend(router.routes)

    def get_openapi(
        self,
        *,
        title: Optional[str] = None,
        version: Optional[str] = None,
        description: Optional[str] = None,
        routes: Optional[List[routing.BaseRoute]] = None,
        tags: Optional[List[Dict[str, Any]]] = None,
        servers: Optional[List[Dict[str, Union[str, Any]]]] = None,
    ) -> Dict[str, Any]:
        if self._openapi_schema_cache:
            return self._openapi_schema_cache
        self.openapi_schema = get_openapi(
            title=title or self.title,
            version=version or self.version,
            description=description or self.description,
            routes=routes or self.routes,
            tags=tags or self.openapi_tags,
            servers=servers or self.servers,
        )
        self._openapi_schema_cache = self.openapi_schema
        return self.openapi_schema

    def openapi(self) -> Dict[str, Any]:
        if not self.openapi_schema:
            self.openapi_schema = self.get_openapi()
        return self.openapi_schema

    def setup(self) -> None:
        """Setup the application."""
        pass

    def mount(self, path: str, app: Any, name: str = None) -> None:
        """Mount an application."""
        pass

    def host(self, host: str = "127.0.0.1", port: int = 8000, **kwargs: Any) -> None:
        """Host the application."""
        pass
