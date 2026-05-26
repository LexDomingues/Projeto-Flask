from Projeto_Flask.controllers.utils import eleva_quadrado
import pytest 
from unittest.mock import Mock, patch
from Projeto_Flask.controllers.utils import requires_role


@pytest.mark.parametrize("input, expected", [
    (2, 4),
    (3, 9),
    (4, 16)
])
def test_eleva_quadrado(input, expected):
    assert eleva_quadrado(input) == expected

def test_requires_role():
    mock_user = Mock()
    mock_user.role.name = "admin"
    mock_get_jwt_identity = patch("Projeto_Flask.controllers.utils.get_jwt_identity")
    mock_db_get_or_404 = patch("Projeto_Flask.controllers.utils.db.get_or_404", return_value=mock_user)
    mock_get_jwt_identity.start()
    mock_db_get_or_404.start()

    decorated_function = requires_role("admin")(lambda: "success")
    result = decorated_function()
    assert result == "success"

    mock_get_jwt_identity.stop()
    mock_db_get_or_404.stop()