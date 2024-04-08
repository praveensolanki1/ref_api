from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="referral program",
        default_version='v1',
        description="to demonstrate referral program",
        terms_of_service="",
        contact=openapi.Contact(email="contact@nn.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)
