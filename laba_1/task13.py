A = [[1,2],[3,4]]
B = [[4,5],[6,7]]

#C = [[0 for x in range(len(A[0]))] for x in range(len(A))] единственный рабочий варик
#я так и не понял как статически задать двумерный массив основываясь на размерах A и B
C = [[0, 0], [0, 0]]
D = [[0, 0], [0, 0]]

# складывание двух матриц
for i in range(len(A)):
    for j in range(len(A[i])):
        C[i][j] = A[i][j] + B[i][j]

# вычитание двух матриц
for i in range(len(A)):
    for j in range(len(A[i])):
        D[i][j] = A[i][j] - B[i][j]

print(C)
print(D)
