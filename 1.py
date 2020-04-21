def maximalRectangle(self, matrix):
    if not matrix or not matrix[0]:
        return 0
    n = len(matrix[0])
    heights = [0] * (n + 1)
    max_m = 0
    for row in matrix:
        for i in range(n):
            heights[i] = heights[i] + 1 if row[i] == '1' else 0
        i = 0
        stack = []
        while i < len(heights):
            if len(stack) == 0 or heights[stack[-1]] <= heights[i]:
                stack.append(i)
                i = i + 1
            else:
                while stack != [] and heights[stack[-1]] > heights[i]:
                    a = stack.pop()
                    if stack == []:
                        max_m = max(max_m, i * heights[a])
                    else:
                        max_m = max(max_m, (i - stack[-1] - 1) * heights[a])
    return max_m

