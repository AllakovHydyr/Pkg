def my_round(x):
    if x >= 0:
        return int(x + 0.5)
    else:
        return int(x - 0.5)


def step_by_step(x1, y1, x2, y2):
    answer = []
    k = (y2 - y1) / (x2 - x1)
    x = my_round(x1)
    b = y1 - x1 * k
    answer.append([x, my_round(y1)])

    while x < x2:
        x += 1
        y = my_round(k * x + b)
        answer.append([x, y])

    return answer


def dda(x1, y1, x2, y2):
    x_beg = my_round(x1)
    y_beg = my_round(y1)
    x_final = my_round(x2)
    y_final = my_round(y2)

    l = max(abs(x_final - x_beg), abs(y_final - y_beg))
    answer = []

    if l == 0:
        return [[x_beg, y_beg]]

    x = x1
    y = y1
    answer.append([x, y])

    for i in range(2, l + 2):
        x += (x2 - x1) / l
        y += (y2 - y1) / l
        answer.append([my_round(x), my_round(y)])

    return answer


def bresenhem(x1, y1, x2, y2):
    x_start = 0
    y_start = 0
    x_final = x2 - x1
    y_final = y2 - y1
    answer = []
    answer.append([x_start + x1, y_start + y1])
    d = 2 * y_final - x_final
    y = y_start

    for x in range(int(x_start + 1), int(x_final + 1)):
        if d < 0:
            answer.append([x + x1, y + y1])
            d += 2 * y_final
        else:
            y += 1
            answer.append([x + x1, y + y1])
            d += 2 * (y_final - x_final)

    return answer


def bresenham_circle(x0, y0, r):
    x = 0
    y = r
    e = 3 - 2 * r

    answer = []
    answer.append([x + x0, y + y0])
    answer.append([x + x0, -y + y0])
    answer.append([-x + x0, y + y0])
    answer.append([-x + x0, -y + y0])
    answer.append([y + x0, x + y0])
    answer.append([y + x0, -x + y0])
    answer.append([-y + x0, x + y0])
    answer.append([-y + x0, -x + y0])

    while x < y:
        if e >= 0:
            e += 4 * (x - y) + 10
            x += 1
            y -= 1
        else:
            e += 4 * x + 6
            x += 1

        answer.append([x + x0, y + y0])
        answer.append([x + x0, -y + y0])
        answer.append([-x + x0, y + y0])
        answer.append([-x + x0, -y + y0])
        answer.append([y + x0, x + y0])
        answer.append([y + x0, -x + y0])
        answer.append([-y + x0, x + y0])
        answer.append([-y + x0, -x + y0])

    return answer


def kastla_pitveya(x1, y1, x2, y2):
    x = x2 - x1 - y2 + y1
    y = y2 - y1

    m1 = 's'
    m2 = 'd'

    i = 0

    while x != y:
        i += 1
        if x > y:
            x -= y
            m2 = m1 + ''.join(reversed(m2))
        else:
            y -= x
            m1 = m2 + ''.join(reversed(m1))

    m = m2 + ''.join(reversed(m1))

    answer = [[x1, y1]]

    for point in m:
        if point == 's':
            x1 += 1
            answer.append([x1, y1])
        elif point == 'd':
            x1 += 1
            y1 += 1
            answer.append([x1, y1])

    return answer


def wu(x_a, y_a, x_b, y_b, m):
    n = 256
    #m = 4
    D = 0
    x1 = 0
    y1 = 0
    x2 = x_b - x_a
    y2 = y_b - y_a

    d = my_round(y2 / x2 * n)

    answer = {(x1 + x_a, y1 + y_a): 0, (x2 + x_a, y2 + y_a): 0}

    while x1 <= x2:
        x1 += 1
        x2 -= 1
        D += d
        if D >= n:
            y1 += 1
            y2 -= 1
            D -= n
        g = int(D / (n / m))
        answer[(x1 + x_a, y1 + y_a)] = g
        answer[(x2 + x_a, y2 + y_a)] = g
        answer[(x1 + x_a, y1 + y_a + 1)] = m - 1 - g
        answer[(x2 + x_a, y2 + y_a - 1)] = m - 1 - g

    return answer
