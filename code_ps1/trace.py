import peak

################################################################################
########################### Class for Tracing Execution ########################
################################################################################

# 创建一个用于记录算法执行轨迹的类
class TraceRecord(object):
    """
    A class for storing the trace of an algorithm, to be exported and displayed
    using the HTML visualizer.
    """

    def __init__(self):
        """
        Initialize the trace to empty.初始化轨迹为空。

        RUNTIME: O(1)
        """

        self.sequence = []

    def getMaximum(self, arguments, maximum): # 记录getMaximum函数被调用的事实
        """
        A function for recording the fact that the getMaximum function of
        some subproblem has been called.

        RUNTIME: O(1)
        """

        self.sequence.append({ # 在轨迹记录中添加一个新的记录
            "type" : "findingMaximum", # 记录类型为"findingMaximum"
            "coords" : arguments # 记录参数
        })

        self.sequence.append({ # 在轨迹记录中添加一个新的记录
            "type" : "foundMaximum", # 记录类型为"foundMaximum"
            "coord" : maximum # 记录最大值
        })

    def getBetterNeighbor(self, neighbor, better): # 记录getBetterNeighbor函数被调用的事实
        """
        A function for recording the fact that the getBetterNeighbor function
        of some subproblem has been called.

        RUNTIME: O(1)
        """

        self.sequence.append({ # 在轨迹记录中添加一个新的记录
            "type" : "findingNeighbor",
            "coord" : neighbor # 记录邻居的坐标
        })

        if (neighbor != better): # 如果邻居不是更好的选项
            self.sequence.append({ # 在轨迹记录中添加一个新的记录
                "type" : "foundNeighbor",
                "coord" : better # 记录更好的选项的坐标
            })

    def setProblemDimensions(self, subproblem): # 记录子问题维度变化的事实
        """
        A function for recording the fact that the dimensions of the currently
        studied subproblem have changed.

        RUNTIME: O(1)
        """

        self.sequence.append({ # 在轨迹记录中添加一个新的记录
            "type" : "subproblem", # 记录类型为"subproblem"
            "startRow" : subproblem.startRow, # 记录子问题的起始行
            "numRows" : subproblem.numRow, # 记录子问题的行数
            "startCol" : subproblem.startCol,  # 记录子问题的起始列
            "numCols" : subproblem.numCol   # 记录子问题的列数
        })

    def setBestSeen(self, bestSeen): # 记录bestSeen变量更新的事实
        """
        A function for recording the fact that the variable "bestSeen" has been
        updated.

        RUNTIME: O(1)
        """

        self.sequence.append({ # 在轨迹记录中添加一个新的记录
            "type" : "bestSeen",    # 记录类型为"bestSeen"
            "coord" : bestSeen # 记录最佳观察到的坐标
        })

    def foundPeak(self, peak): # 记录峰值被找到的事实
        """
        A function for recording the fact that the peak has been found.

        RUNTIME: O(1)
        """

        self.sequence.append({ # 在轨迹记录中添加一个新的记录
            "type" : "foundPeak", # 记录类型为"foundPeak"
            "coord" : peak  # 记录峰值的坐标
        })
