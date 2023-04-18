import os
import uuid


def get_upload_path_for_icon(instance, filename):
    """
    Генерирует уникальное имя файла и возвращает путь для сохранения файла.
    """
    ext = filename.split('.')[-1].lower()
    if ext not in ['jpg', 'png', 'jpeg', 'svg']:
        raise ValueError('Недопустимое расширение файла. Разрешены только jpg, jpeg, png, svg.')
    filename = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join(
        'icons',  # имя папки для сохранения файлов
        filename  # имя файла
    )
    return path


def get_upload_path_for_users(instance, filename):
    """
    Генерирует уникальное имя файла и возвращает путь для сохранения файла.
    """
    ext = filename.split('.')[-1].lower()
    if ext not in ['jpg', 'png', 'jpeg', 'svg']:
        raise ValueError('Недопустимое расширение файла. Разрешены только jpg, jpeg, png, svg.')
    filename = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join(
        'users',  # имя папки для сохранения файлов
        filename  # имя файла
    )
    return path
