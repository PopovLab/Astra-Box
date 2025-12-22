
import zipfile
import re
from pathlib import Path
from typing import List, Optional, Tuple, Union
import io
from io import BytesIO
import f90nml

class TimestampFilesManager:
    """
    Класс для работы с файлами в zip-архиве, имена которых являются float числами секунд.
    Пример имен файлов: 0.123.dat
    """
    
    def __init__(self, zip_path: Union[str, Path] , internal_path: str = ""):
        """
        Инициализация менеджера.
        Args:
            zip_path: Путь к zip-архиву
            internal_path: Путь внутри архива (если файлы находятся в поддиректории)
        """
        self.zip_path = Path(zip_path)
        self.internal_path = internal_path.rstrip('/') + '/' if internal_path else ""
        
        if not self.zip_path.exists():
            raise FileNotFoundError(f"Zip архив не существует: {zip_path}")
        
        self._cache: List[str] | None = None
        self._zip_ref = None

    def __enter__(self):
        """Контекстный менеджер для автоматического закрытия zip-архива."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Закрытие zip-архива при выходе из контекста."""
        self.close()
    
    def _open_zip(self):
        """Открыть zip-архив для чтения."""
        #if self._zip_ref is None:
        #    self._zip_ref = zipfile.ZipFile(self.zip_path, 'r')
        return zipfile.ZipFile(self.zip_path, 'r')
    
    def close(self):
        """Закрыть zip-архив."""
        print('close')
        if self._zip_ref is not None:
            self._zip_ref.close()
            self._zip_ref = None   
            print('close zip_ref')     

    def _refresh_cache(self) -> None:
        """Обновить кэш файлов из zip-архива."""
        print('Обновить кэш файлов')
        with self._open_zip() as zip_ref:
            # Получаем все файлы, которые находятся по указанному пути
            all_files = zip_ref.namelist()
            #print(all_files)
            # Фильтруем только файлы из нужной директории
            filtered_files = []
            for file_path in all_files:
                # Пропускаем директории
                if file_path.endswith('/'):
                    continue
                # Проверяем, что файл находится в нужной директории
                if file_path.startswith(self.internal_path):
                    # Получаем относительный путь
                    rel_path = file_path[len(self.internal_path):]
                    # Игнорируем файлы во вложенных папках
                    if '/' not in rel_path and '\\' not in rel_path:
                        filtered_files.append(file_path)
            print(filtered_files)
            #print(filtered_files.sort())
            self._cache = sorted(filtered_files)

    def files(self) -> List[str]:
        if self._cache is None:
            self._refresh_cache()
        return self._cache
        

    def _parse_timestamp(self, filename: str) -> Optional[float]:
        """
        Извлечь временную метку из имени файла.
        Args:
            filename: Имя файла (например, "0.123.dat")
        Returns:
            Числовую метку в секундах или None если не удалось распарсить
        """
        try:
            # Берем часть имени файла до расширения
            name_without_ext = Path(filename).stem
            return float(name_without_ext)
        except (ValueError, AttributeError):
            pass
        return None            
    
    def get_timestamp_files(self) -> List[Tuple[str, float]]:
        """
        Получить все файлы с временными метками из zip-архива.
        
        Returns:
            Список кортежей (имя_файла_в_архиве, временная_метка)
        """

        result = []
        for file_path in self.files():
            # Получаем только имя файла (без пути)
            filename = Path(file_path).name
            timestamp = self._parse_timestamp(filename)
            if timestamp is not None:
                result.append((file_path, timestamp))
        
        return result    
    
    def count_files(self) -> int:
        """
        Returns:
            Количество файлов
        """
        return len(self.get_timestamp_files())    
    
    def get_timestamp_range(self) -> Tuple[float, float]:
        """
        Получить диапазон временных меток.
        Returns:
            Кортеж (минимальная_метка, максимальная_метка) 
            или None если файлы отсутствуют
        """
        files = self.get_timestamp_files()
        
        timestamps = [timestamp for _, timestamp in files]
        return (min(timestamps), max(timestamps))    
    
    def find_closest_file(self, target_time: float) -> Tuple[str, float, float]:
        """
        Найти файл, наиболее близкий к указанной временной метке.
        Args:
            target_time: Целевая временная метка
        Returns:
            Кортеж (имя_файла_в_архиве, временная_метка, разница_во_времени)
            или None если файлы отсутствуют
        """
        files = self.get_timestamp_files()
        if not files:
            return None
        
        # Находим файл с минимальной разницей во времени
        closest_file = min(files, key=lambda x: abs(x[1] - target_time))
        file_path, timestamp = closest_file
        time_diff = timestamp - target_time
        
        return (file_path, timestamp, time_diff)    
    
    def read_nml_file(self, target_time: float) -> dict:
        """
        Прочитать содержимое nml-файла из zip-архива.
        Args:
            file_path: Путь к файлу внутри архива
        Returns:
            Содержимое nml-файла в виде dict
        """
        file_path, _, _  = self.find_closest_file(target_time)
        if Path(file_path).suffix != '.nml': return {}

        with self._open_zip() as zip_ref:
            with io.TextIOWrapper(zip_ref.open(file_path), encoding="utf-8") as file:
                return f90nml.read(file)            