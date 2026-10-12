import pytest
from string_utils import StringUtils

string_utils = StringUtils()


# ==========================================
# Тесты для метода capitalize
# ==========================================
@pytest.mark.positive
@pytest.mark.parametrize("input_str, expected", [
    ("skypro", "Skypro"),
    ("hello world", "Hello world"),
    ("python", "Python"),
])
def test_capitalize_positive(input_str, expected):
    assert string_utils.capitalize(input_str) == expected


@pytest.mark.negative
@pytest.mark.parametrize("input_str, expected", [
    ("123abc", "123abc"),
    ("", ""),
    ("   ", "   "),
])
def test_capitalize_negative(input_str, expected):
    assert string_utils.capitalize(input_str) == expected


@pytest.mark.negative
def test_capitalize_none():
    with pytest.raises(AttributeError):
        string_utils.capitalize(None)


# ==========================================
# Тесты для метода trim
# ==========================================
@pytest.mark.positive
@pytest.mark.parametrize("input_str, expected", [
    ("   skypro", "skypro"),
    (" skypro", "skypro"),
    ("skypro   ", "skypro   "),  # Удаляет только в начале
])
def test_trim_positive(input_str, expected):
    assert string_utils.trim(input_str) == expected


@pytest.mark.negative
@pytest.mark.parametrize("input_str, expected", [
    ("", ""),
    ("   ", ""),
    ("skypro", "skypro"),
])
def test_trim_negative(input_str, expected):
    assert string_utils.trim(input_str) == expected


@pytest.mark.negative
def test_trim_none():
    with pytest.raises(AttributeError):
        string_utils.trim(None)


# ==========================================
# Тесты для метода contains
# ==========================================
@pytest.mark.positive
@pytest.mark.parametrize("input_str, symbol, expected", [
    ("SkyPro", "S", True),
    ("SkyPro", "y", True),
    ("SkyPro", "U", False),
    ("SkyPro", "u", False),
])
def test_contains_positive(input_str, symbol, expected):
    assert string_utils.contains(input_str, symbol) == expected


@pytest.mark.negative
@pytest.mark.parametrize("input_str, symbol", [
    (None, "S"),
    ("SkyPro", None),
])
def test_contains_none(input_str, symbol):
    with pytest.raises((AttributeError, TypeError)):
        string_utils.contains(input_str, symbol)


@pytest.mark.negative
def test_contains_empty_symbol():
    # Поиск пустой строки всегда возвращает True (индекс 0)
    assert string_utils.contains("SkyPro", "") is True


# ==========================================
# Тесты для метода delete_symbol
# ==========================================
@pytest.mark.positive
@pytest.mark.parametrize("input_str, symbol, expected", [
    ("SkyPro", "k", "SyPro"),
    ("SkyPro", "Pro", "Sky"),
    ("hello", "l", "heo"),
    ("hello", "z", "hello"),  # Символа нет, строка не меняется
])
def test_delete_symbol_positive(input_str, symbol, expected):
    assert string_utils.delete_symbol(input_str, symbol) == expected


@pytest.mark.negative
@pytest.mark.parametrize("input_str, symbol", [
    (None, "a"),
    ("hello", None),
])
def test_delete_symbol_none(input_str, symbol):
    with pytest.raises((AttributeError, TypeError)):
        string_utils.delete_symbol(input_str, symbol)


@pytest.mark.negative
def test_delete_symbol_empty():
    # Удаление пустой строки не меняет исходную строку
    assert string_utils.delete_symbol("hello", "") == "hello"