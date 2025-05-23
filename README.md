# DuelPong

Гра написана за допомогою ШІ Claude [https://claude.ai/](https://claude.ai/)

## Опис

- Гра для двох гравців (але якщо ви самотній, можна грати самому)
- Гравці керують ракетками, що рухаються вертикально
- М'яч відбивається від верхньої та нижньої стінок
- Якщо м'яч торкається лівої або правої стіни, очко отримує протилежний від даної стіни гравець
- Рахунок відображається у верхній частині екрану кольором відповідного гравця

![Знімок екрана (119)](https://github.com/user-attachments/assets/75ad59ef-20ff-4b78-9a88-be09f08c01ef)

## Керування

- Лівий гравець (зелений):
  - W - вгору
  - S - вниз
- Правий гравець (синій):
  - ↑ (стрілка вгору) - вгору
  - ↓ (стрілка вниз) - вниз

- Пауза: Кнопка "Пауза" або клавіша Escape
- Налаштування сили руху м'яча: Кнопка "Налаштування" у правому верхньому куті

## Встановлення

1. Клонуйте репозиторій:

    ```bash
    git clone https://github.com/BlackPencil-69/DuelPong.git
    cd DuelPong
    ```

2. Встановіть залежності:

    ```bash
    pip install -r requirements.txt
    ```

3. Запустіть гру:

    ```bash
    python DuelPong.py
    ```

Або

- Скачайте і розпакуйте репозиторій
- Відкрийте термінал та вставте:

    ```bash
    pip install pygame
    ```

## Автор

[BlackPencil-69](https://github.com/BlackPencil-69)

Надихнуто класичною грою Pong, розробленою Atari у 1972 році.
