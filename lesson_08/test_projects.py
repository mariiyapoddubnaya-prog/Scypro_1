import os
import uuid
import pytest
from dotenv import load_dotenv
from yougile_client import YougileAPIClient


# Загружаем переменные из файла .env при запуске
load_dotenv()


@pytest.fixture(scope="module")
def api_client():
    token = os.getenv("YOUGILE_TOKEN")
    assert token, ("Переменная окружения YOUGILE_TOKEN не установлена."
                   " Проверьте файл .env")
    return YougileAPIClient(token=token)

@pytest.fixture
def project_id(api_client):
    """Фикстура создает проект перед тестом и удаляет его после."""
    unique_title = f"TestProject_{uuid.uuid4().hex[:8]}"

    # Создаем проект
    response = api_client.create_project(title=unique_title)
    assert response.status_code == 201, \
        f"Не удалось создать проект: {response.text}"
    created_id = response.json()["id"]

    yield created_id

    # Teardown: помечаем проект как удаленный после завершения теста
    api_client.update_project(project_id=created_id, deleted=True)


# ==================== POST ТЕСТЫ ====================

def test_create_project_positive(api_client):
    unique_title = f"NewProject_{uuid.uuid4().hex[:8]}"
    idempotency_key = uuid.uuid4().hex

    response = api_client.create_project(
        title=unique_title,
        idempotency_key=idempotency_key
    )

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    # Проверка идемпотентности (повторный запрос с тем же ключом)
    response_retry = api_client.create_project(
        title=unique_title,
        idempotency_key=idempotency_key
    )
    assert response_retry.status_code == 201
    assert response_retry.json()["id"] == data["id"]


def test_create_project_negative(api_client):
    # Попытка создать проект без обязательного поля title
    response = api_client.create_project(title="")

    # Ожидаем ошибку валидации (обычно 400 или 422)
    assert response.status_code in [400, 422]


# ==================== GET ТЕСТЫ ====================

def test_get_project_positive(api_client, project_id):
    response = api_client.get_project(project_id)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == project_id
    assert "title" in data


def test_get_project_negative(api_client):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = api_client.get_project(fake_id)

    assert response.status_code == 404


# ==================== PUT ТЕСТЫ ====================

def test_update_project_positive(api_client, project_id):
    new_title = f"UpdatedProject_{uuid.uuid4().hex[:8]}"

    response = api_client.update_project(project_id=project_id,
                                         title=new_title)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == project_id


def test_update_project_negative(api_client):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = api_client.update_project(project_id=fake_id, title="Fake")

    assert response.status_code == 404
