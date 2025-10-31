import numpy as np
import matplotlib.pyplot as plt

class FuzzySet:
    # класс нечеткого множества с треугольной функцией принадлежности
    def __init__(self, name, a, b, c):
        self.name = name
        self.a = a
        self.b = b
        self.c = c

    def membership(self, x):
        # расчет степени принадлежности значения x
        if x <= self.a:
            return 0.0
        elif self.a < x <= self.b:
            if self.a == self.b:
                return 1.0 if x == self.a else 0.0
            return (x - self.a) / (self.b - self.a)
        elif self.b < x < self.c:
            if self.b == self.c:
                return 1.0 if x == self.b else 0.0
            return (self.c - x) / (self.c - self.b)
        else:
            return 0.0

    def display_info(self, x=None):
        # вывод информации о нечетком множестве
        print(f"Нечеткое множество: {self.name}")
        print(f"Параметры треугольной функции: a={self.a}, b={self.b}, c={self.c}")
        if x is not None:
            degree = self.membership(x)
            print(f"Степень принадлежности значения {x}: {degree:.3f}")
        print("-" * 50)

    def plot(self, x_range, ax=None, show_plot=True, current_value=None):
        # визуализация функции принадлежности
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))

        x_vals = np.linspace(x_range[0], x_range[1], 1000)
        y_vals = [self.membership(x) for x in x_vals]

        ax.plot(x_vals, y_vals, label=self.name, linewidth=2)
        ax.fill_between(x_vals, y_vals, alpha=0.3)

        if current_value is not None:
            degree = self.membership(current_value)
            ax.axvline(x=current_value, color='red', linestyle='--', alpha=0.7)
            ax.plot(current_value, degree, 'ro', markersize=8)
            ax.annotate(f'x={current_value}\nμ={degree:.3f}',
                        xy=(current_value, degree),
                        xytext=(10, 10), textcoords='offset points',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

        ax.set_xlabel('Значение')
        ax.set_ylabel('Степень принадлежности')
        ax.set_title(f'Функция принадлежности: {self.name}')
        ax.grid(True, alpha=0.3)
        ax.legend()

        if show_plot:
            plt.show()

        return ax

class WaterQualitySystem:
    # система оценки качества воды
    def __init__(self):
        # инициализация нечетких множеств
        self.cleanliness_sets = [
            FuzzySet("Чистая", 0, 0, 25),
            FuzzySet("Слегка загрязненная", 15, 35, 55),
            FuzzySet("Загрязненная", 45, 65, 85),
            FuzzySet("Сильно загрязненная", 75, 100, 100)
        ]

        self.temperature_sets = [
            FuzzySet("Холодная", 0, 0, 15),
            FuzzySet("Прохладная", 10, 17, 24),
            FuzzySet("Теплая", 20, 27, 34),
            FuzzySet("Горячая", 30, 40, 40)
        ]

    def evaluate_cleanliness(self, pollution_level):
        # оценка чистоты воды по уровню загрязнения
        print("ОЦЕНКА ЧИСТОТЫ ВОДЫ")
        print(f"Уровень загрязнения: {pollution_level} мг/л")
        print("=" * 50)

        results = []
        for fuzzy_set in self.cleanliness_sets:
            degree = fuzzy_set.membership(pollution_level)
            results.append((fuzzy_set.name, degree))
            fuzzy_set.display_info(pollution_level)

        max_degree = max(results, key=lambda x: x[1])
        print(f"Наиболее вероятная категория: {max_degree[0]} (степень принадлежности: {max_degree[1]:.3f})")

        return results

    def evaluate_temperature(self, temperature):
        # оценка температуры воды
        print("\nОЦЕНКА ТЕМПЕРАТУРЫ ВОДЫ")
        print(f"Температура воды: {temperature}°C")
        print("=" * 50)

        results = []
        for fuzzy_set in self.temperature_sets:
            degree = fuzzy_set.membership(temperature)
            results.append((fuzzy_set.name, degree))
            fuzzy_set.display_info(temperature)

        max_degree = max(results, key=lambda x: x[1])
        print(f"Наиболее вероятная категория: {max_degree[0]} (степень принадлежности: {max_degree[1]:.3f})")

        return results

    def plot_all_cleanliness_sets(self, current_value=None):
        # график всех множеств для чистоты воды
        fig, ax = plt.subplots(figsize=(12, 6))

        for fuzzy_set in self.cleanliness_sets:
            x_vals = np.linspace(0, 100, 1000)
            y_vals = [fuzzy_set.membership(x) for x in x_vals]
            ax.plot(x_vals, y_vals, label=fuzzy_set.name, linewidth=2)
            ax.fill_between(x_vals, y_vals, alpha=0.2)

        if current_value is not None:
            ax.axvline(x=current_value, color='red', linestyle='--', linewidth=2,
                       label=f'Текущее значение: {current_value}')
            for fuzzy_set in self.cleanliness_sets:
                degree = fuzzy_set.membership(current_value)
                if degree > 0:
                    ax.plot(current_value, degree, 'ro', markersize=8)
                    ax.annotate(f'{fuzzy_set.name}\nμ={degree:.3f}',
                                xy=(current_value, degree),
                                xytext=(10, 10), textcoords='offset points',
                                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

        ax.set_xlabel('Уровень загрязнения (мг/л)')
        ax.set_ylabel('Степень принадлежности')
        ax.set_title('Нечеткие множества для оценки чистоты воды')
        ax.grid(True, alpha=0.3)
        ax.legend()
        plt.tight_layout()
        plt.show()

    def plot_all_temperature_sets(self, current_value=None):
        # график всех множеств для температуры воды
        fig, ax = plt.subplots(figsize=(12, 6))

        for fuzzy_set in self.temperature_sets:
            x_vals = np.linspace(0, 40, 1000)
            y_vals = [fuzzy_set.membership(x) for x in x_vals]
            ax.plot(x_vals, y_vals, label=fuzzy_set.name, linewidth=2)
            ax.fill_between(x_vals, y_vals, alpha=0.2)

        if current_value is not None:
            ax.axvline(x=current_value, color='red', linestyle='--', linewidth=2,
                       label=f'Текущее значение: {current_value}')
            for fuzzy_set in self.temperature_sets:
                degree = fuzzy_set.membership(current_value)
                if degree > 0:
                    ax.plot(current_value, degree, 'ro', markersize=8)
                    ax.annotate(f'{fuzzy_set.name}\nμ={degree:.3f}',
                                xy=(current_value, degree),
                                xytext=(10, 10), textcoords='offset points',
                                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

        ax.set_xlabel('Температура (°C)')
        ax.set_ylabel('Степень принадлежности')
        ax.set_title('Нечеткие множества для оценки температуры воды')
        ax.grid(True, alpha=0.3)
        ax.legend()
        plt.tight_layout()
        plt.show()

    def plot_all_sets(self):
        # общий график всех нечетких множеств
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        for fuzzy_set in self.cleanliness_sets:
            x_vals = np.linspace(0, 100, 1000)
            y_vals = [fuzzy_set.membership(x) for x in x_vals]
            ax1.plot(x_vals, y_vals, label=fuzzy_set.name, linewidth=2)
            ax1.fill_between(x_vals, y_vals, alpha=0.2)
        ax1.set_xlabel('Уровень загрязнения (мг/л)')
        ax1.set_ylabel('Степень принадлежности')
        ax1.set_title('Оценка чистоты воды')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        for fuzzy_set in self.temperature_sets:
            x_vals = np.linspace(0, 40, 1000)
            y_vals = [fuzzy_set.membership(x) for x in x_vals]
            ax2.plot(x_vals, y_vals, label=fuzzy_set.name, linewidth=2)
            ax2.fill_between(x_vals, y_vals, alpha=0.2)
        ax2.set_xlabel('Температура (°C)')
        ax2.set_ylabel('Степень принадлежности')
        ax2.set_title('Оценка температуры воды')
        ax2.grid(True, alpha=0.3)
        ax2.legend()

        plt.tight_layout()
        plt.show()

def main():
    # основная функция программы
    system = WaterQualitySystem()

    print("Лабораторная работа №2: Нечёткая логика")
    print("Система оценки качества воды")
    print("=" * 50)

    while True:
        print("\nМеню:")
        print("1. Оценить чистоту воды")
        print("2. Оценить температуру воды")
        print("3. Показать все нечеткие множества")
        print("4. Выход")

        choice = input("Выберите действие (1-4): ").strip()

        if choice == '1':
            try:
                pollution = float(input("Введите уровень загрязнения воды (0-100 мг/л): "))
                if 0 <= pollution <= 100:
                    results = system.evaluate_cleanliness(pollution)
                    show_graph = input("Показать график? (y/n): ").strip().lower()
                    if show_graph == 'y':
                        system.plot_all_cleanliness_sets(pollution)
                else:
                    print("Ошибка: уровень загрязнения должен быть в диапазоне 0-100 мг/л")
            except ValueError:
                print("Ошибка: введите числовое значение")

        elif choice == '2':
            try:
                temp = float(input("Введите температуру воды (0-40°C): "))
                if 0 <= temp <= 40:
                    results = system.evaluate_temperature(temp)
                    show_graph = input("Показать график? (y/n): ").strip().lower()
                    if show_graph == 'y':
                        system.plot_all_temperature_sets(temp)
                else:
                    print("Ошибка: температура должна быть в диапазоне 0-40°C")
            except ValueError:
                print("Ошибка: введите числовое значение")

        elif choice == '3':
            print("\nВизуализация всех нечетких множеств...")
            system.plot_all_sets()

        elif choice == '4':
            print("Выход из программы...")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()