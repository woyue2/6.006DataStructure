import trace

################################################################################
########################### Peak问题的类 ############################
################################################################################

class PeakProblem(object):
    """
    表示峰值查找问题的实例的类。
    """

    def __init__(self, array, bounds):
        """
        初始化PeakProblem类的实例的方法。
        接受一个数组和一个指示要包含哪些行的参数。

        运行时间：O(1)
        """

        (startRow, startCol, numRow, numCol) = bounds

        self.array = array
        self.bounds = bounds
        self.startRow = startRow
        self.startCol = startCol
        self.numRow = numRow
        self.numCol = numCol

    def get(self, location):
        """
        返回给定位置在数组中的值，偏移坐标为(startRow, startCol)。

        运行时间：O(1)
        """

        (r, c) = location
        if not (0 <= r and r < self.numRow):
            return 0
        if not (0 <= c and c < self.numCol):
            return 0
        return self.array[self.startRow + r][self.startCol + c]

    def getBetterNeighbor(self, location, trace = None):
        """
        如果(r, c)有一个更好的邻居，则返回邻居。否则，返回位置(r, c)。

        运行时间：O(1)
        """

        (r, c) = location
        best = location

        if r - 1 >= 0 and self.get((r - 1, c)) > self.get(best):
            best = (r - 1, c)
        if c - 1 >= 0 and self.get((r, c - 1)) > self.get(best):
            best = (r, c - 1)
        if r + 1 < self.numRow and self.get((r + 1, c)) > self.get(best):
            best = (r + 1, c)
        if c + 1 < self.numCol and self.get((r, c + 1)) > self.get(best):
            best = (r, c + 1)

        if not trace is None: trace.getBetterNeighbor(location, best)

        return best
    
    def getMaximum(self, locations, trace = None):
        """
        在当前问题中找到具有最大值的位置。

        运行时间：O(len(locations))
        """
   
        (bestLoc, bestVal) = (None, 0)
    
        for loc in locations:
            if bestLoc is None or self.get(loc) > bestVal:
                (bestLoc, bestVal) = (loc, self.get(loc))
    
        if not trace is None: trace.getMaximum(locations, bestLoc)

        return bestLoc

    def isPeak(self, location):
        """
        如果给定位置是当前子问题中的峰值，则返回True。

        运行时间：O(1)
        """

        return (self.getBetterNeighbor(location) == location)

    def getSubproblem(self, bounds):
        """
        返回具有给定边界的子问题。边界是一个四元组数字：(起始行，起始列，行数，列数)。

        运行时间：O(1)
        """

        (sRow, sCol, nRow, nCol) = bounds
        newBounds = (self.startRow + sRow, self.startCol + sCol, nRow, nCol)
        return PeakProblem(self.array, newBounds)

        def getSubproblemContaining(self, boundList, location):
            """
            返回包含给定位置的子问题。在boundList中选择满足约束条件的第一个子问题，
            然后使用getSubproblem()构造子问题。

            运行时间：O(len(boundList))
            """

            (row, col) = location
            for (sRow, sCol, nRow, nCol) in boundList:
                if sRow <= row and row < sRow + nRow:
                    if sCol <= col and col < sCol + nCol:
                        return self.getSubproblem((sRow, sCol, nRow, nCol))

            # 不应该到达这里
            return self

        def getLocationInSelf(self, problem, location):
            """
            将给定问题中的位置重新映射到调用此函数的问题中的相同位置。

            运行时间：O(1)
            """

            (row, col) = location
            newRow = row + problem.startRow - self.startRow
            newCol = col + problem.startCol - self.startCol
            return (newRow, newCol)

    ################################################################################
    ################################ 辅助方法 ################################
    ################################################################################

    def getDimensions(array):
        """
        获取二维数组的维度。第一维是列表中的项数；第二维是最短行的长度。
        这确保了任何小于结果边界的位置(row, col)实际上都映射到数组中的有效位置。

        运行时间：O(len(array))
        """

        rows = len(array)
        cols = 0
        
        for row in array:
            if len(row) > cols:
                cols = len(row)
        
        return (rows, cols)

    def createProblem(array):
        """
        使用从数组中使用getDimensions函数派生的边界，构造PeakProblem对象的实例。

        运行时间：O(len(array))
        """

        (rows, cols) = getDimensions(array)
        return PeakProblem(array, (0, 0, rows, cols))
