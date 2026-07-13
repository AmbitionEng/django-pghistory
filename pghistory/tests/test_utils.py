from django.db import models

from pghistory import models as pgh_models


def test_middleware_events_user_field_foreign_key(mocker):
    mocker.patch("pghistory.models.settings.AUTH_USER_MODEL", "auth.User")
    mocker.patch("pghistory.models.apps.is_installed", return_value=True)
    field = pgh_models._middleware_events_user_field()
    assert isinstance(field, models.ForeignKey)


def test_middleware_events_user_field_textfield(mocker):
    mocker.patch("pghistory.models.settings.AUTH_USER_MODEL", "myapp.User")
    mocker.patch("pghistory.models.apps.is_installed", return_value=False)
    field = pgh_models._middleware_events_user_field()
    assert isinstance(field, models.TextField)


def test_middleware_events_user_field_textfield_no_auth_user_model(mocker):
    mocker.patch("pghistory.models.settings.AUTH_USER_MODEL", None)
    field = pgh_models._middleware_events_user_field()
    assert isinstance(field, models.TextField)


def test_middleware_events_user_field_textfield_invalid_auth_user_model(mocker):
    mocker.patch("pghistory.models.settings.AUTH_USER_MODEL", "invalid")
    field = pgh_models._middleware_events_user_field()
    assert isinstance(field, models.TextField)
