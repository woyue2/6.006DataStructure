import peak 
import trace

################################################################################
################################## Algorithms ##################################
################################################################################

def algorithm1(problem, trace = None):
    """
    算法1：使用分治法寻找峰值

    Parameters:
        problem (Problem): 问题实例
        trace (Trace, optional): 跟踪对象，用于记录算法执行过程中的信息。默认为None。

    Returns:
        tuple: 峰值的位置坐标

    """
    # 如果问题为空，则直接返回
    if problem.numRow <= 0 or problem.numCol <= 0:
        return None

    # 递归子问题将涉及一半的列数
    mid = problem.numCol // 2

    # 两个子问题的信息
    (subStartR, subNumR) = (0, problem.numRow)
    (subStartC1, subNumC1) = (0, mid)
    (subStartC2, subNumC2) = (mid + 1, problem.numCol - (mid + 1))

    subproblems = []
    subproblems.append((subStartR, subStartC1, subNumR, subNumC1))
    subproblems.append((subStartR, subStartC2, subNumR, subNumC2))

    # 获取划分列中的所有位置列表
    divider = crossProduct(range(problem.numRow), [mid])

    # 在划分列中找到最大值
    bestLoc = problem.getMaximum(divider, trace)

    # 检查我们在划分线上找到的最大值是否有更好的邻居（不能在划分线上，因为我们知道该位置是划分线上的最佳位置）
    neighbor = problem.getBetterNeighbor(bestLoc, trace)

    # 这是一个峰值，所以返回它
    if neighbor == bestLoc:
        if not trace is None: trace.foundPeak(bestLoc)
        return bestLoc
   
    # 否则，找出包含邻居的子问题，并在该子问题中递归
    sub = problem.getSubproblemContaining(subproblems, neighbor)
    if not trace is None: trace.setProblemDimensions(sub)
    result = algorithm1(sub, trace)
    return problem.getLocationInSelf(sub, result)

def algorithm2(problem, location = (0, 0), trace = None):
    """
    算法2：使用贪心法寻找峰值

    Parameters:
        problem (Problem): 问题实例
        location (tuple, optional): 当前位置坐标。默认为(0, 0)。
        trace (Trace, optional): 跟踪对象，用于记录算法执行过程中的信息。默认为None。

    Returns:
        tuple: 峰值的位置坐标

    """
    # 如果问题为空，则直接返回
    if problem.numRow <= 0 or problem.numCol <= 0:
        return None

    nextLocation = problem.getBetterNeighbor(location, trace)

    if nextLocation == location:
        # 没有更好的邻居，所以返回该峰值
        if not trace is None: trace.foundPeak(location)
        return location
    else:
        # 存在更好的邻居，所以移动到邻居位置并递归
        return algorithm2(problem, nextLocation, trace)

def algorithm3(problem, bestSeen = None, trace = None):
    """
    算法3：使用分治法和贪心法结合寻找峰值

    Parameters:
        problem (Problem): 问题实例
        bestSeen (tuple, optional): 已经找到的最佳峰值位置坐标。默认为None。
        trace (Trace, optional): 跟踪对象，用于记录算法执行过程中的信息。默认为None。

    Returns:
        tuple: 峰值的位置坐标

    """
    # 如果问题为空，则直接返回
    if problem.numRow <= 0 or problem.numCol <= 0:
        return None

    midRow = problem.numRow // 2
    midCol = problem.numCol // 2

    # 首先，获取所有子问题的列表
    subproblems = []

    (subStartR1, subNumR1) = (0, midRow)
    (subStartR2, subNumR2) = (midRow + 1, problem.numRow - (midRow + 1))
    (subStartC1, subNumC1) = (0, midCol)
    (subStartC2, subNumC2) = (midCol + 1, problem.numCol - (midCol + 1))

    subproblems.append((subStartR1, subStartC1, subNumR1, subNumC1))
    subproblems.append((subStartR1, subStartC2, subNumR1, subNumC2))
    subproblems.append((subStartR2, subStartC1, subNumR2, subNumC1))
    subproblems.append((subStartR2, subStartC2, subNumR2, subNumC2))

    # 在交叉区域（中间行和中间列的组合）中找到最佳位置
    cross = []

    cross.extend(crossProduct([midRow], range(problem.numCol)))
    cross.extend(crossProduct(range(problem.numRow), [midCol]))

    crossLoc = problem.getMaximum(cross, trace)
    neighbor = problem.getBetterNeighbor(crossLoc, trace)

    # 根据这个新的最大值更新到目前为止看到的最佳峰值
    if bestSeen is None or problem.get(neighbor) > problem.get(bestSeen):
        bestSeen = neighbor
        if not trace is None: trace.setBestSeen(bestSeen)

    # 如果我们看不到更好的邻居，则返回
    if neighbor == crossLoc:
        if not trace is None: trace.foundPeak(crossLoc)
        return crossLoc

    # 找出包含到目前为止看到的最大数的子问题，并递归
    sub = problem.getSubproblemContaining(subproblems, bestSeen)
    newBest = sub.getLocationInSelf(problem, bestSeen)
    if not trace is None: trace.setProblemDimensions(sub)
    result = algorithm3(sub, newBest, trace)
    return problem.getLocationInSelf(sub, result)

def algorithm4(problem, bestSeen = None, rowSplit = True, trace = None):
    """
    算法4：使用分治法和贪心法结合，交替按行或按列划分，寻找峰值

    Parameters:
        problem (Problem): 问题实例
        bestSeen (tuple, optional): 已经找到的最佳峰值位置坐标。默认为None。
        rowSplit (bool, optional): 是否按行划分子问题。默认为True。
        trace (Trace, optional): 跟踪对象，用于记录算法执行过程中的信息。默认为None。

    Returns:
        tuple: 峰值的位置坐标

    """
    # 如果问题为空，则直接返回
    if problem.numRow <= 0 or problem.numCol <= 0:
        return None

    subproblems = []
    divider = []

    if rowSplit:
        # 递归子问题将涉及一半的行数
        mid = problem.numRow // 2

        # 两个子问题的信息
        (subStartR1, subNumR1) = (0, mid)
        (subStartR2, subNumR2) = (mid + 1, problem.numRow - (mid + 1))
        (subStartC, subNumC) = (0, problem.numCol)

        subproblems.append((subStartR1, subStartC, subNumR1, subNumC))
        subproblems.append((subStartR2, subStartC, subNumR2, subNumC))

        # 获取划分行中的所有位置列表
        divider = crossProduct([mid], range(problem.numCol))
    else:
        # 递归子问题将涉及一半的列数
        mid = problem.numCol // 2

        # 两个子问题的信息
        (subStartR, subNumR) = (0, problem.numRow)
        (subStartC1, subNumC1) = (0, mid)
        (subStartC2, subNumC2) = (mid + 1, problem.numCol - (mid + 1))

        subproblems.append((subStartR, subStartC1, subNumR, subNumC1))
        subproblems.append((subStartR, subStartC2, subNumR, subNumC2))

        # 获取划分列中的所有位置列表
        divider = crossProduct(range(problem.numRow), [mid])

    # 在划分行或列中找到最大值
    bestLoc = problem.getMaximum(divider, trace)
    neighbor = problem.getBetterNeighbor(bestLoc, trace)

    # 根据这个新的最大值更新到目前为止看到的最佳峰值
    if bestSeen is None or problem.get(neighbor) > problem.get(bestSeen):
        bestSeen = neighbor
        if not trace is None: trace.setBestSeen(bestSeen)

    # 当我们知道我们找到了一个峰值时返回
    if neighbor == bestLoc and problem.get(bestLoc) >= problem.get(bestSeen):
        if not trace is None: trace.foundPeak(bestLoc)
        return bestLoc

    # 找出包含到目前为止看到的最大数的子问题，并递归，交替在行和列上划分
    sub = problem.getSubproblemContaining(subproblems, bestSeen)
    newBest = sub.getLocationInSelf(problem, bestSeen)
    if not trace is None: trace.setProblemDimensions(sub)
    result = algorithm4(sub, newBest, not rowSplit, trace)
    return problem.getLocationInSelf(sub, result)


################################################################################
################################ Helper Methods ################################
################################################################################


def crossProduct(list1, list2):
    """
    返回两个列表的笛卡尔积，即所有可能的组合。

    Parameters:
        list1 (list): 第一个列表
        list2 (list): 第二个列表

    Returns:
        list: 笛卡尔积列表

    """
    answer = []
    for a in list1:
        for b in list2:
            answer.append ((a, b))
    return answer

