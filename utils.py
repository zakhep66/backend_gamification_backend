import os
import uuid


def get_upload_path_for_icon(instance, filename):
    """
    Генерирует уникальное имя файла и возвращает путь для сохранения.
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
    Генерирует уникальное имя файла для аватарки и возвращает путь для сохранения.
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


def get_upload_path_for_market_image(instance, filename):
    """
    Генерирует уникальное имя файла для продукта и возвращает путь для сохранения.
    """
    ext = filename.split('.')[-1].lower()
    if ext not in ['jpg', 'png', 'jpeg', 'svg']:
        raise ValueError('Недопустимое расширение файла. Разрешены только jpg, jpeg, png, svg.')
    filename = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join(
        'product',  # имя папки для сохранения файлов
        filename  # имя файла
    )
    return path


def get_upload_path_for_emoji(instance, filename):
    """
    Генерирует уникальное имя файла для продукта и возвращает путь для сохранения.
    """
    ext = filename.split('.')[-1].lower()
    if ext not in ['jpg', 'png', 'jpeg', 'svg']:
        raise ValueError('Недопустимое расширение файла. Разрешены только jpg, jpeg, png, svg.')
    filename = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join(
        'emoji',  # имя папки для сохранения файлов
        filename  # имя файла
    )
    return path
