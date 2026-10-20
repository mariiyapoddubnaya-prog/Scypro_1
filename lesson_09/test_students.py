import uuid
import pytest
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import Student


# Фикстура для создания таблиц (если их вдруг нет) и очистки сессии
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def db_session():
    """Создает сессию БД и гарантирует её закрытие после теста."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()  # Откатываем незавершенные транзакции
        session.close()


def test_create_student(db_session: Session):
    """Тест на добавление новой сущности в БД."""
    unique_name = f"TestStudent_Create_{uuid.uuid4().hex[:6]}"

    # 1. Создаем и добавляем студента
    new_student = Student(name=unique_name, age=20, group_name="Group_A")
    db_session.add(new_student)
    db_session.commit()
    db_session.refresh(new_student)

    # 2. Проверяем, что студент действительно добавлен
    assert new_student.id is not None
    student_in_db = (
        db_session.query(Student).filter(Student.name == unique_name).first())
    assert student_in_db is not None
    assert student_in_db.age == 20

    # 3. Очистка: удаляем созданного студента
    db_session.delete(student_in_db)
    db_session.commit()


def test_update_student(db_session: Session):
    """Тест на изменение существующей сущности в БД."""
    unique_name = f"TestStudent_Update_{uuid.uuid4().hex[:6]}"

    # 1. Создаем студента для изменения
    new_student = Student(name=unique_name, age=20, group_name="Group_A")
    db_session.add(new_student)
    db_session.commit()
    db_session.refresh(new_student)

    # 2. Изменяем данные
    new_student.age = 21
    new_student.group_name = "Group_B"
    db_session.commit()
    db_session.refresh(new_student)

    # 3. Проверяем, что данные обновились
    student_in_db = (
        db_session.query(Student).filter(Student.id == new_student.id).first())
    assert student_in_db.age == 21
    assert student_in_db.group_name == "Group_B"

    # 4. Очистка
    db_session.delete(student_in_db)
    db_session.commit()


def test_delete_student(db_session: Session):
    """Тест на удаление сущности из БД."""
    unique_name = f"TestStudent_Delete_{uuid.uuid4().hex[:6]}"

    # 1. Создаем студента для удаления
    new_student = Student(name=unique_name, age=20, group_name="Group_A")
    db_session.add(new_student)
    db_session.commit()
    db_session.refresh(new_student)
    student_id = new_student.id

    # 2. Удаляем студента
    db_session.delete(new_student)
    db_session.commit()

    # 3. Проверяем, что студент больше не существует в БД
    student_in_db = (
        db_session.query(Student).filter(Student.id == student_id).first())
    assert student_in_db is None
