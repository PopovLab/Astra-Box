# kernel.py
import time
import threading
from queue import Queue
from loguru import logger

from AstraBox.Task import Task
from AstraBox.WorkSpace import WorkSpace
from core import wsl

class Kernel:
    """Каждое ядро имеет свой логгер, очередь сообщений и файловый лог."""

    _next_id = 1
    _lock = threading.Lock()

    def __init__(self):
        with Kernel._lock:
            self.kernel_id = Kernel._next_id
            Kernel._next_id += 1

        self.message_queue = Queue()
        self.is_running = False
        self._thread = None

        # Создаём локальный логгер с привязкой к kernel_id
        self.log = logger.bind(kernel_id=self.kernel_id)

        # Настраиваем обработчики: файл + очередь
        self._setup_handlers()

    def _setup_handlers(self):
        """Добавляем обработчики loguru для этого ядра."""
        # 1. Файловый обработчик (пишет в kernel_X.log)
        self.log.add(
            f"kernel_{self.kernel_id}.log",
            rotation="1 MB",
            retention="3 days",
            encoding="utf-8",
            level="INFO",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            colorize=False
        )

        # 2. Обработчик для отправки сообщений в очередь GUI
        #    Используем filter, чтобы обрабатывались только сообщения этого ядра
        self.log.add(
            self._queue_sink,
            level="INFO",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | <level>{message}</level>",
            filter=lambda record: record["extra"].get("kernel_id") == self.kernel_id,
            colorize=False
        )

    def _queue_sink(self, message):
        """Функция-приёмник: кладёт сообщение в очередь."""
        self.message_queue.put(message)

    def start(self, **kwargs) -> None:
        if self.is_running:
            raise RuntimeError(f"Kernel {self.kernel_id} уже выполняет вычисления")

        self.is_running = True
        self._thread = threading.Thread(
            target=self._run,
            kwargs= kwargs,
            daemon=True
        )
        self._thread.start()

    def _run(self, **kwargs) -> None:
        try:
            match kwargs:
                case {"steps": int(s), "delay": float(d)}:
                    self.log.info(f"Цикл на {s} шагов с паузой {d} сек.")
                    self._run_test(s, d)

                case {"work_space": WorkSpace() as w, "task": Task() as t, "options": str(o)}:
                    self._run_astra(w, t, o)

                case _:
                    print("Неизвестная конфигурация параметров")
                    print(kwargs)
                    self.log.error("Неизвестная конфигурация параметров")
        except Exception as e:
            self.log.exception("Ошибка в потоке вычислений")
        finally:
            self.is_running = False
            self.message_queue.put("__DONE__\n")  # маркер завершения
                

    def _run_test(self, steps: int, delay: float) -> None:
        self.log.info("Вычисления начаты")
        for step in range(1, steps + 1):
            time.sleep(delay)
            progress = int(step / steps * 100)
            self.log.info(f"Шаг {step}/{steps} ({progress}%) завершён.")
        self.log.info("Вычисления успешно завершены")


    def _run_astra(self, work_space:WorkSpace, task:Task , options:str) -> None:

        self.log.info("try start ASTRA")
        runner = wsl.create_runner(self.log)
        #worker = AstraWorker(work_space, task, options)
        #worker.execute(runner)
        #self.log.info(f"Шаг {5}/{15} ({50}%) завершён.")
        self.log.info("Вычисления успешно завершены")
