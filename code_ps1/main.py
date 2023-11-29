import sys  # 导入sys模块，用于处理Python运行时的环境（命令行参数等）
import peak  # 导入peak模块，用于处理峰值问题
import trace  # 导入trace模块，用于跟踪算法的执行
import algorithms  # 导入algorithms模块，包含各种算法的实现
import json  # 导入json模块，用于处理JSON数据
import utils  # 导入utils模块，包含各种实用工具函数

# 以下是主函数的定义

def loadProblem(file = "problem.py", variable = "problemMatrix"):
    """
    从python文件中加载矩阵，并根据它构建PeakProblem对象。
    """
    namespace = dict()  # 创建一个空字典，用于存储执行python文件后的命名空间
    with open(file) as handle:  # 打开文件
        exec(handle.read(), namespace)  # 执行文件中的python代码
    return peak.createProblem(namespace[variable])  # 从命名空间中获取矩阵，并创建PeakProblem对象

def main():  # 定义主函数
    if len(sys.argv) > 1:  # 如果命令行参数数量大于1（除了脚本名之外还有其他参数）
        problem = loadProblem(sys.argv[1])  # 使用第一个命令行参数作为文件名，加载问题
    else:  # 如果没有其他命令行参数
        problem = loadProblem(utils.getOpenFilename("problem.py"))  # 使用用户选择的文件名，加载问题

    # 运行所有算法，收集跟踪信息并打印结果
    algorithmList = [("Algorithm 1", algorithms.algorithm1),
                     ("Algorithm 2", algorithms.algorithm2),
                     ("Algorithm 3", algorithms.algorithm3),
                     ("Algorithm 4", algorithms.algorithm4)]  # 定义算法列表

    steps = []  # 创建一个空列表，用于存储每个算法的步骤数
    
    for (name, function) in algorithmList:  # 遍历算法列表
        tracer = trace.TraceRecord()  # 创建一个TraceRecord对象，用于跟踪算法的执行
        peak = function(problem, trace = tracer)  # 执行算法，并传入TraceRecord对象
        steps.append(tracer.sequence)
        
        status = "is NOT a peak (INCORRECT!)"
        if problem.isPeak(peak):
            status = "is a peak"

        print(name + " : " + str(peak) + " => " + status)

    # 将跟踪信息写入文件
    with open("trace.jsonp", "w") as traceFile:
        traceFile.write("parse(")

        json.dump({
            "input" : problem.array,
            "steps" : steps
        }, traceFile)

        traceFile.write(")")

if __name__ == "__main__":
    main()
