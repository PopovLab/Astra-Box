# kernel.py
import time
import threading
from queue import Queue
from loguru import logger
from returns.pipeline import is_successful

from AstraBox import Config, RaceZip
from AstraBox.Task import Task, TaskList
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

        astra_profile = Config.get_astra_profile(task.astra_profile)
        print(astra_profile)
        if not runner.check_astra_profile(astra_profile):
            self.log.error('ASTRA is not available')
            return
        astra_user = astra_profile["profile"]
        astra_home = astra_profile["home"]

        wsl_path = f'{astra_home}/{astra_user}'
        self.log.info(f'start task {task.name}')
        
        runner.clear_work_folders(astra_home, astra_user)
        
        res = RaceZip.create_race_zip(work_space, task)
        if is_successful(res): 
            zip_file= res.unwrap()     
            runner.put_file(zip_file, wsl_path)
            runner.exec(wsl_path, f'unzip -o race_data.zip')   

            task_list = None
            
            if task.exp == '*.*':
                task_list = TaskList(main_task= task)
                #for sub_task in self.sub_task_generaton(task):
                #    astra_cmd = f'./run_astra.sh {astra_user} {sub_task.exp} {sub_task.equ} {option}'
                #    print(sub_task)
                #    WSL.start_exec(self.astra_home, astra_cmd)
                #    self.pack_task_results(sub_task)
                #    self.mk_work_folders()
                #    task_list.tasks.append(sub_task)
            else:

                astra_cmd = f'./run_astra.sh {astra_user} {task.exp} {task.equ} {options}'
                print(astra_cmd)
                runner.start_exec(astra_home, astra_cmd)
 
                self.log.info('----- pack data -------')
                runner.exec(wsl_path, f'zip -r race_data.zip dat')
                runner.exec(wsl_path, f'zip -r race_data.zip lhcd')

            self.log.info('finish')
        else:
            self.log.error(res)
        self.log.info("Вычисления успешно завершены")
