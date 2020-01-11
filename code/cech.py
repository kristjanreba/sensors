import rips
import random
import math


def circle(p1,p2,p3):
    a = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)
    b = math.sqrt((p1[0] - p3[0]) ** 2 + (p1[1] - p3[1]) ** 2 + (p1[2] - p3[2]) ** 2)
    c = math.sqrt((p2[0] - p3[0]) ** 2 + (p2[1] - p3[1]) ** 2 + (p2[2] - p3[2]) ** 2)
    cosa = (a ** 2 + b ** 2 - c ** 2) / (2 * b * a)
    (x1, y1) = (0, 0)
    (x2, y2) = (a, 0)
    (x3, y3) = (cosa * b, math.sin(math.acos(cosa)) * b)
    A = x1 * (y2 - y3) - y1 * (x2 - x3) + x2*y3 - x3*y2
    B = (x1*x1 + y1*y1) * (y3 - y2) + (x2*x2 + y2*y2) * (y1 - y3) + (x3*x3 + y3*y3) * (y2 - y1)
    C = (x1*x1 + y1*y1) * (x2 - x3) + (x2*x2 + y2*y2) * (x3 - x1) + (x3*x3 + y3*y3) * (x1 - x2)
    D = (x1*x1 + y1*y1) * (x3*y2 - x2*y3) + (x2*x2 + y2*y2) * (x1*y3 - x3*y1) + (x3*x3 + y3*y3) * (x2*y1 - x1*y2)
    (c, r) = ((-B / (2 * A), -C / (2 * A)), (B ** 2 + C ** 2 - 4 * A * D) / (4 * A ** 2))
    alpha = (c[0] * y3 - c[1] * x3) / (x2 * y3 - y2 * x3)
    beta = (-c[0] * y2 + c[1] * x2) / (x2 * y3 - y2 * x3)
    return ((p1[0] + alpha * (p2[0] - p1[0]) + beta * (p3[0] - p1[0]),
             p1[1] + alpha * (p2[1] - p1[1]) + beta * (p3[1] - p1[1]),
             p1[2] + alpha * (p2[2] - p1[2]) + beta * (p3[2] - p1[2])), r)


def sphere(p1, p2, p3, p4):
    (a1, a2, a3) = p1
    (b1, b2, b3) = p2
    (c1, c2, c3) = p3
    (d1, d2, d3) = p4
    f1 = ((a1 ** 2 + a2 ** 2 + a3 ** 2) * (c2 * d3 + d2 * b3 + b2 * c3 - d2 * c3 - b2 * d3 - c2 * b3) + (
                b1 ** 2 + b2 ** 2 + b3 ** 2) * (d2 * c3 + c2 * a3 + a2 * d3 - c2 * d3 - a2 * c3 - d2 * a3) + (
                      c1 ** 2 + c2 ** 2 + c3 ** 2) * (a2 * b3 + b2 * d3 + d2 * a3 - b2 * a3 - d2 * b3 - a2 * d3) + (
                      d1 ** 2 + d2 ** 2 + d3 ** 2) * (b2 * a3 + a2 * c3 + c2 * b3 - a2 * b3 - c2 * a3 - b2 * c3)) / (
                     2 * a1 * (c2 * d3 + d2 * b3 + b2 * c3 - d2 * c3 - b2 * d3 - c2 * b3) + b1 * (
                         d2 * c3 + c2 * a3 + a2 * d3 - c2 * d3 - a2 * c3 - d2 * a3) + c1 * (
                                 a2 * b3 + b2 * d3 + d2 * a3 - b2 * a3 - d2 * b3 - a2 * d3) + d1 * (
                                 b2 * a3 + a2 * c3 + c2 * b3 - a2 * b3 - c2 * a3 - b2 * c3))
    f2 = ((a1 ** 2 + a2 ** 2 + a3 ** 2) * (c1 * d3 + d1 * b3 + b1 * c3 - d1 * c3 - b1 * d3 - c1 * b3) + (
                b1 ** 2 + b2 ** 2 + b3 ** 2) * (d1 * c3 + c1 * a3 + a1 * d3 - c1 * d3 - a1 * c3 - d1 * a3) + (
                      c1 ** 2 + c2 ** 2 + c3 ** 2) * (a1 * b3 + b1 * d3 + d1 * a3 - b1 * a3 - d1 * b3 - a1 * d3) + (
                      d1 ** 2 + d2 ** 2 + d3 ** 2) * (b1 * a3 + a1 * c3 + c1 * b3 - a1 * b3 - c1 * a3 - b1 * c3)) / (
                     2 * a2 * (c1 * d3 + d1 * b3 + b1 * c3 - d1 * c3 - b1 * d3 - c1 * b3) + b2 * (
                         d1 * c3 + c1 * a3 + a1 * d3 - c1 * d3 - a1 * c3 - d1 * a3) + c2 * (
                                 a1 * b3 + b1 * d3 + d1 * a3 - b1 * a3 - d1 * b3 - a1 * d3) + d2 * (
                                 b1 * a3 + a1 * c3 + c1 * b3 - a1 * b3 - c1 * a3 - b1 * c3))
    f3 = ((a1 ** 2 + a2 ** 2 + a3 ** 2) * (c1 * d2 + d1 * b2 + b1 * c2 - d1 * c2 - b1 * d2 - c1 * b2) + (
                b1 ** 2 + b2 ** 2 + b3 ** 2) * (d1 * c2 + c1 * a2 + a1 * d2 - c1 * d2 - a1 * c2 - d1 * a2) + (
                      c1 ** 2 + c2 ** 2 + c3 ** 2) * (a1 * b2 + b1 * d2 + d1 * a2 - b1 * a2 - d1 * b2 - a1 * d2) + (
                      d1 ** 2 + d2 ** 2 + d3 ** 2) * (b1 * a2 + a1 * c2 + c1 * b2 - a1 * b2 - c1 * a2 - b1 * c2)) / (
                     2 * a3 * (c1 * d2 + d1 * b2 + b1 * c2 - d1 * c2 - b1 * d2 - c1 * b2) + b3 * (
                         d1 * c2 + c1 * a2 + a1 * d2 - c1 * d2 - a1 * c2 - d1 * a2) + c3 * (
                                 a1 * b2 + b1 * d2 + d1 * a2 - b1 * a2 - d1 * b2 - a1 * d2) + d3 * (
                                 b1 * a2 + a1 * c2 + c1 * b2 - a1 * b2 - c1 * a2 - b1 * c2))
    return ((f1, f2, f3), (a1 - f1) ** 2 + (a2 - f2) ** 2 + (a3 - f3) ** 2)


def minBall(tau, ni):
    if len(tau) == 0 or len(ni) == 4:
        ln = len(ni)
        if ln == 0:
            return ((0, 0, 0), 0)
        if ln == 1:
            return (ni[0], 0)
        elif ln == 2:
            # B((x,y),r^2)
            p0, p1 = ni[0], ni[1]
            return (((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, (p0[2] + p1[2]) / 2),
                    ((p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2 + (p0[2] - p1[2]) ** 2) / 4)
        elif ln == 3:
            a = (ni[0][0] - ni[1][0]) ** 2 + (ni[0][1] - ni[1][1]) ** 2 + (ni[0][2] - ni[1][2]) ** 2
            b = (ni[0][0] - ni[2][0]) ** 2 + (ni[0][1] - ni[2][1]) ** 2 + (ni[0][2] - ni[2][2]) ** 2
            c = (ni[2][0] - ni[1][0]) ** 2 + (ni[2][1] - ni[1][1]) ** 2 + (ni[2][2] - ni[1][2]) ** 2
            if max([a, b, c]) * 2 >= sum([a, b, c]):
                if a == max([a, b, c]):
                    return minBall([], [ni[0], ni[1]])
                elif b == max([a, b, c]):
                    return minBall([], [ni[0], ni[2]])
                else:
                    return minBall([], [ni[2], ni[1]])
            else:
                return circle(ni[0], ni[1], ni[2])
        else:
            B = circle(ni[0], ni[1], ni[2])
            if (ni[3][0] - B[0][0]) ** 2 + (ni[3][1] - B[0][1]) ** 2 + (ni[3][2] - B[0][2]) ** 2 <= B[1]:
                return B
            B = circle(ni[0], ni[1], ni[3])
            if (ni[2][0] - B[0][0]) ** 2 + (ni[2][1] - B[0][1]) ** 2 + (ni[2][2] - B[0][2]) ** 2 <= B[1]:
                return B
            B = circle(ni[0], ni[2], ni[3])
            if (ni[1][0] - B[0][0]) ** 2 + (ni[1][1] - B[0][1]) ** 2 + (ni[1][2] - B[0][2]) ** 2 <= B[1]:
                return B
            B = circle(ni[1], ni[2], ni[3])
            if (ni[0][0] - B[0][0]) ** 2 + (ni[0][1] - B[0][1]) ** 2 + (ni[0][2] - B[0][2]) ** 2 <= B[1]:
                return B
            return sphere(ni[0], ni[1], ni[2], ni[3])
    else:
        u = tau[random.randint(0, len(tau) - 1)]
        t = [v for v in tau if v != u]
        B = minBall(t, ni)
        if (u[0] - B[0][0]) ** 2 + (u[1] - B[0][1]) ** 2 + (u[2] - B[0][2]) ** 2 > B[1]:
            B = minBall(t, ni + [u])
        return B


def cech(S, epsilon):
    candidates = rips.VR(S, 2 * epsilon)
    for i, sxes in candidates.items():
        candidates[i] = [sx for sx in sxes if minBall([S[j] for j in sx], [])[1] <= epsilon ** 2]
    return candidates
