import pytest
from authentication.validators import ContainsLetterValidator, ContainsNumberValidator
from django.core.exceptions import ValidationError


def test_should_raise_an_error_if_no_letter_in_password():
    sut = ContainsLetterValidator
    password = '123456'
    with pytest.raises(ValidationError):
        sut.validate(ContainsLetterValidator, password, None)

    assert sut.get_help_text(ContainsLetterValidator) == 'Your password must contain at least one upper or lower case letter.'


def test_should_raise_an_error_if_no_number_in_password():
    sut = ContainsNumberValidator
    password = 'qwerty'
    with pytest.raises(ValidationError):
        sut.validate(ContainsNumberValidator, password, None)

    assert sut.get_help_text(ContainsNumberValidator) == 'Your password must contain at least one number.'