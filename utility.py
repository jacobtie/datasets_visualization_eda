def reduceByKey(arr):
    res = []
    for val in arr:
        found = False
        for i,r in enumerate(res):
            if r[0] == val:
                r[1] += 1
                found = True
                break
        if not found:
            res.append([val, 1])
    return res