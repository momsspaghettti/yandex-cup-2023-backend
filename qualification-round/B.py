def get_modified_string(s: str) -> str:
    yandex = "Yandex"
    cup = "Cup"
    yandex_cost_to_min_ind: dict[int, int] = {}
    cup_cost_to_max_ind: dict[int, int] = {}
    for i in range(len(s)):
        if i + len(yandex) <= len(s) and len(yandex_cost_to_min_ind) < 6:
            yandex_cost = get_make_str_cost(s[i:], yandex)
            if yandex_cost not in yandex_cost_to_min_ind:
                yandex_cost_to_min_ind[yandex_cost] = i
        if i >= len(yandex) and i + len(cup) <= len(s):
            cup_cost = get_make_str_cost(s[i:], cup)
            cup_cost_to_max_ind[cup_cost] = i

    yandex_ind: int = 0
    cup_ind: int = 0
    for cost in range(0, len(yandex) + len(cup) + 1):
        need_to_break = False
        for yandex_cost in range(0, min(len(yandex), cost) + 1):
            cup_cost = cost - yandex_cost
            yandex_ind = yandex_cost_to_min_ind.get(yandex_cost, len(s))
            cup_ind = cup_cost_to_max_ind.get(cup_cost, -1)
            if yandex_ind + len(yandex) <= cup_ind:
                need_to_break = True
                break
        if need_to_break:
            break
    return s[:yandex_ind] + yandex + s[yandex_ind + len(yandex):cup_ind] + cup + s[cup_ind + len(cup):]


def get_make_str_cost(s: str, target: str) -> int:
    res = 0
    for i in range(len(target)):
        if s[i] != target[i]:
            res += 1
    return res


print(get_modified_string(input()))
