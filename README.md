# Astra-Box

Python wrapper for ASTRA

Required for run: python 3.12, poetry, ASTRA on WSL2.

Doc ([rus](https://temper8.github.io/Astra-Box/))



![](/docs/media/main.png)


## Установка Astra-Box для Windows

1. Установить python для Windows:

    скачать дистрибутив с сайта https://www.python.org/

    запустить и выбрать опцию `add python.exe to PATH`


2. Установить менеджер зависимостей Poetry

    ```
    pip install poetry
    ```

3. Клонировать репозиторий Astra-Box
    ```
    git clone https://github.com/PopovLab/Astra-Box.git
    ```
3. Установить зависимости для Astra-Box

    ```
    cd my_projects\Astra-Box
    poetry install 
    ```

4. можно запустить 
    ```
    run.bat
    ```


## Установка Astra-Box для Ubuntu

1. Нужен Python 3.12 (самое просто использовать Ubuntu 24.04)

2.  установка pip  и poetry
    ```
    sudo apt install python3-pip

    sudo apt install python3-poetry

    sudo apt install python3-tk

    ```

3. клонировать репозиторий
    ```
    git clone https://github.com/PopovLab/Astra-Box.git
    ```

4. инициализация
    ```
    cd Astra-Box
    poetry install
    ```


5. запуск
    ```
    poetry run python main.py
    ```

    