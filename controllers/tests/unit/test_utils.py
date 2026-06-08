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

def test_requires_role(mocker):
    mock_user = mocker.Mock()
    mock_user.role.name = "admin"

    mocker.patch("Projeto_Flask.controllers.utils.get_jwt_identity")
    mocker.patch("Projeto_Flask.controllers.utils.db.get_or_404", return_value=mock_user)
    decorated_function = requires_role("admin")(lambda: "Success")

    result = decorated_function()
    assert result == "Success"
    