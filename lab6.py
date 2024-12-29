import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Исходные координаты вершин буквы "А"
vertices = np.array([
    [0, 0, 0],  # Низ
    [0.5, 1, 0],  # Средняя точка верха
    [1, 0, 0],  # Низ справа
    [0.25, 0.5, 0],  # Левый перекладин
    [0.75, 0.5, 0]  # Правый перекладин
])

edges = [
    (0, 1), (1, 2), (0, 3), (3, 4), (4, 2)
]

# Трансформация матриц
def scale_matrix(sx, sy, sz):
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])

def translation_matrix(tx, ty, tz):
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])

def rotation_matrix(axis, angle):
    axis = axis / np.linalg.norm(axis)
    x, y, z = axis
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [c + (1 - c) * x**2, (1 - c) * x * y - s * z, (1 - c) * x * z + s * y, 0],
        [(1 - c) * y * x + s * z, c + (1 - c) * y**2, (1 - c) * y * z - s * x, 0],
        [(1 - c) * z * x - s * y, (1 - c) * z * y + s * x, c + (1 - c) * z**2, 0],
        [0, 0, 0, 1]
    ])

def apply_transformation(vertices, matrix):
    homogeneous_vertices = np.hstack((vertices, np.ones((vertices.shape[0], 1))))
    transformed_vertices = homogeneous_vertices @ matrix.T
    return transformed_vertices[:, :3]

# Построение графика

def create_3d_figure(vertices, edges):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    for edge in edges:
        x = [vertices[edge[0], 0], vertices[edge[1], 0]]
        y = [vertices[edge[0], 1], vertices[edge[1], 1]]
        z = [vertices[edge[0], 2], vertices[edge[1], 2]]
        ax.plot(x, y, z, color='blue')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    plt.show()

# Основной цикл программы
if __name__ == '__main__':
    while True:
        print("\nТекущий 3D-объект отображается. Выберите действие:")
        print("1. Масштабировать объект")
        print("2. Переместить объект")
        print("3. Повернуть объект")
        print("4. Выйти")
        
        choice = input("Введите номер действия: ")

        if choice == '1':
            sx = float(input("Введите коэффициент масштабирования по X: "))
            sy = float(input("Введите коэффициент масштабирования по Y: "))
            sz = float(input("Введите коэффициент масштабирования по Z: "))
            matrix = scale_matrix(sx, sy, sz)
            vertices = apply_transformation(vertices, matrix)
            create_3d_figure(vertices, edges)

        elif choice == '2':
            tx = float(input("Введите смещение по X: "))
            ty = float(input("Введите смещение по Y: "))
            tz = float(input("Введите смещение по Z: "))
            matrix = translation_matrix(tx, ty, tz)
            vertices = apply_transformation(vertices, matrix)
            create_3d_figure(vertices, edges)

        elif choice == '3':
            x = float(input("Введите X-составляющую оси вращения: "))
            y = float(input("Введите Y-составляющую оси вращения: "))
            z = float(input("Введите Z-составляющую оси вращения: "))
            angle = float(input("Введите угол вращения (в градусах): "))
            matrix = rotation_matrix(np.array([x, y, z]), np.radians(angle))
            vertices = apply_transformation(vertices, matrix)
            create_3d_figure(vertices, edges)

        elif choice == '4':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор, попробуйте снова.")
