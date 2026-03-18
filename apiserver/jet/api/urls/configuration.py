from django.urls import path


from jet.api.views import ConfigurationEndpoint

urlpatterns = [
    path(
        "configs/",
        ConfigurationEndpoint.as_view(),
        name="configuration",
    ),
]