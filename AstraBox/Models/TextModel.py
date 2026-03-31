from abc import ABC, abstractmethod

class TextModel(ABC):
    """Abstract base class for all models."""

    def __init__(self, data):
        """Constructor that accepts the model's internal data."""
        self.text = data

    @classmethod
    def from_file(cls, file_path):
        """Creates a model instance by loading data from a file."""
        with file_path.open('r') as f:
            data = f.read()
        return cls(data)

    @abstractmethod
    def _load_data_from_file(file_path):
        """A static or class method for reading data from a file.
           Must be implemented in a subclass.
        """
        pass

    def save(self, file_path):
        """Saves the current model instance to a file."""
        self._save_data_to_file(file_path)

    @abstractmethod
    def _save_data_to_file(self, file_path):
        """Abstract method for saving data to a file.
           Must be implemented in a subclass
        """
        pass