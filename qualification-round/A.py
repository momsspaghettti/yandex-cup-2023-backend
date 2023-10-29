def get_second_points_sum(first_points: list[int]) -> int:
    prefix_sums: list[int] = []
    for point in first_points:
        if point == 0:
            continue
        if len(prefix_sums) == 0:
            prefix_sums.append(point)
        else:
            prefix_sums.append(prefix_sums[-1] + point)
    res: int = 0
    ind: int = 0
    for point in first_points:
        if point == 0:
            continue
        res += point ** 2
        res += prefix_sums[min(ind + point, len(prefix_sums) - 1)] - prefix_sums[ind]
        ind += 1
    return res


_, m, *_ = map(int, input().split())
print(get_second_points_sum(list(map(int, input().split()))[:m]))
