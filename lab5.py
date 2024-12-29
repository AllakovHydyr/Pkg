import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np


# Алгоритм Сазерленда-Коэна для отсечения отрезков
def sutherland_cohen_clip(x1, y1, x2, y2, xmin, ymin, xmax, ymax):
    INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 4, 8

    def compute_code(x, y):
        code = INSIDE
        if x < xmin:
            code |= LEFT
        elif x > xmax:
            code |= RIGHT
        if y < ymin:
            code |= BOTTOM
        elif y > ymax:
            code |= TOP
        return code

    code1 = compute_code(x1, y1)
    code2 = compute_code(x2, y2)
    accept = False

    while True:
        if code1 == 0 and code2 == 0:  # Оба конца внутри
            accept = True
            break
        elif code1 & code2 != 0:  # Оба конца вне в одном регионе
            break
        else:
            code_out = code1 if code1 != 0 else code2
            x, y = 0, 0

            if code_out & TOP:
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax
            elif code_out & BOTTOM:
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin
            elif code_out & RIGHT:
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax
            elif code_out & LEFT:
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin

            if code_out == code1:
                x1, y1 = x, y
                code1 = compute_code(x1, y1)
            else:
                x2, y2 = x, y
                code2 = compute_code(x2, y2)

    if accept:
        return (x1, y1, x2, y2)
    else:
        return None


# Алгоритм отсечения выпуклого многоугольника
def clip_polygon(polygon, clip_rect):
    xmin, ymin, xmax, ymax = clip_rect
    edges = [
        ((xmin, ymin), (xmin, ymax)),  # Левая сторона
        ((xmin, ymax), (xmax, ymax)),  # Верхняя сторона
        ((xmax, ymax), (xmax, ymin)),  # Правая сторона
        ((xmax, ymin), (xmin, ymin)),  # Нижняя сторона
    ]

    def is_inside(point, edge):
        (x, y), ((x1, y1), (x2, y2)) = point, edge
        return (x2 - x1) * (y - y1) >= (y2 - y1) * (x - x1)

    def intersect(p1, p2, edge):
        (x1, y1), (x2, y2) = p1, p2
        (xe1, ye1), (xe2, ye2) = edge
        a1, b1 = ye2 - ye1, xe1 - xe2
        c1 = a1 * xe1 + b1 * ye1
        a2, b2 = y2 - y1, x1 - x2
        c2 = a2 * x1 + b2 * y1
        det = a1 * b2 - a2 * b1
        if det == 0:
            return None
        x = (b2 * c1 - b1 * c2) / det
        y = (a1 * c2 - a2 * c1) / det
        return (x, y)

    output_list = polygon
    for edge in edges:
        input_list = output_list
        output_list = []
        if not input_list:
            break
        s = input_list[-1]
        for e in input_list:
            if is_inside(e, edge):
                if not is_inside(s, edge):
                    output_list.append(intersect(s, e, edge))
                output_list.append(e)
            elif is_inside(s, edge):
                output_list.append(intersect(s, e, edge))
            s = e
    return output_list


# Функция для визуализации
def visualize(lines, clipped_lines, polygon, clipped_polygon, clip_rect):
    xmin, ymin, xmax, ymax = clip_rect

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(xmin - 10, xmax + 10)
    ax.set_ylim(ymin - 10, ymax + 10)
    ax.set_aspect('equal', adjustable='box')

    rect = Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                     linewidth=1, edgecolor='red', facecolor='none')
    ax.add_patch(rect)

    for line in lines:
        x1, y1, x2, y2 = line
        ax.plot([x1, x2], [y1, y2], 'b--', label="Исходные линии")

    for line in clipped_lines:
        if line:
            x1, y1, x2, y2 = line
            ax.plot([x1, x2], [y1, y2], 'g-', linewidth=2, label="Отсеченные линии")

    if polygon:
        polygon.append(polygon[0])
        px, py = zip(*polygon)
        ax.plot(px, py, 'b--', label="Исходный многоугольник")

    if clipped_polygon:
        clipped_polygon.append(clipped_polygon[0])
        px, py = zip(*clipped_polygon)
        ax.plot(px, py, 'g-', linewidth=2, label="Отсеченный многоугольник")

    plt.legend()
    plt.show()


# Чтение данных из файла
def read_input(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    n = int(lines[0].strip())
    segments = [tuple(map(float, line.strip().split())) for line in lines[1:n + 1]]
    clip_rect = tuple(map(float, lines[n + 1].strip().split()))
    polygon = [tuple(map(float, line.strip().split())) for line in lines[n + 2:]]
    return segments, clip_rect, polygon


# Основная функция
def main():
    file_path = "input.txt"  # Замените на путь к вашему файлу
    lines, clip_rect, polygon = read_input(file_path)

    if not lines:
        print("Ошибка: отрезки не заданы.")
        return

    if not polygon:
        print("Ошибка: многоугольник не задан.")
        return

    clipped_lines = [sutherland_cohen_clip(*line, *clip_rect) for line in lines]
    clipped_polygon = clip_polygon(polygon, clip_rect)

    visualize(lines, clipped_lines, polygon, clipped_polygon, clip_rect)


if __name__ == "__main__":
    main()