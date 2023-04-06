import os
import uuid


def get_upload_path(instance, filename):
    """
    Генерирует уникальное имя файла и возвращает путь для сохранения файла.
    """
    ext = filename.split('.')[-1].lower()
    if ext not in ['jpg', 'png']:
        raise ValueError('Недопустимое расширение файла. Разрешены только jpg и png.')
    filename = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join(
        'uploads/media',  # имя папки для сохранения файлов
        filename  # имя файла
    )
    return path


def get_upload_path_for_users(instance, filename):
    """
    Генерирует уникальное имя файла и возвращает путь для сохранения файла.
    """
    ext = filename.split('.')[-1].lower()
    if ext not in ['jpg', 'png']:
        raise ValueError('Недопустимое расширение файла. Разрешены только jpg и png.')
    filename = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join(
        'uploads/users',  # имя папки для сохранения файлов
        filename  # имя файла
    )
    return path
