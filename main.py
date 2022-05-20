import copy


def Initial_Conditions(cant_be_min):
    final_graph_list = []
    vertexes = [1, 2, 3, 4, 5, 6, 7, 8]
    matr = [[0, 1, 1, 0, 1, 1, 0, 0], #1
            [1, 0, 0, 0, 0, 1, 0, 2], #2
            [1, 0, 0, 1, 0, 0, 0, 0], #3
            [0, 0, 1, 0, 1, 0, 0, 0], #4
            [1, 0, 0, 1, 0, 0, 0, 0], #5
            [1, 1, 0, 0, 0, 0, 1, 0], #6
            [0, 0, 0, 0, 0, 1, 0, 1], #7
            [0, 2, 0, 0, 0, 0, 1, 0]] #8
    power_of_subgraphs = [3, 3, 2]
    if cant_be_min != []:
        print()
    Print_Matrix(matr, vertexes, power_of_subgraphs, cant_be_min, final_graph_list)


def Print_Matrix (matr, vertexes, power_of_subgraphs, cant_be_min, final_graph_list):
    print("\tМатриця зв'язності має вигляд:")
    print(vertexes)
    print("________________________")

    for i in matr:
        print(i)
    Local_Degrees(matr, vertexes, power_of_subgraphs, cant_be_min, final_graph_list)

def Local_Degrees(matr, vertexes, power_of_subgraphs, cant_be_min, final_graph_list):
    if len(power_of_subgraphs) > 1:
        print("\tЛокальні ступені кожної вершини:")
        local_degrees = []
        width = len(matr)
        for i in range(width):
            local_degrees.append(0)
            for j in matr[i]:
                local_degrees[i] += j
        print(local_degrees)

        if 0 in local_degrees:
            print("\t\tОберемо іншу мінімальну вершину...")
            Initial_Conditions(cant_be_min)
        else:
            power_of_subgraphs_2 = copy.deepcopy(power_of_subgraphs)
            x = []
            Δ = []
            min = local_degrees[0]
            width = len(matr)
            vertex_min_number = Min_Vertex(min, local_degrees, width, vertexes, cant_be_min)
            cant_be_min.append(vertex_min_number)
            x.append(vertex_min_number)
            # print(cant_be_min)
            while len(Δ) <= len(power_of_subgraphs_2):
                # print("here")
                vertex_numbers = New_Plural(matr, vertex_min_number, vertexes)
                set_combination = []
                set_combination.append(vertex_min_number)
                for i in range(len(vertex_numbers)):
                    set_combination.append(vertex_numbers[i])
                print("\tОб'єднані множини:", set_combination)
                x.append(Connectivity_Factor(vertex_min_number, set_combination, vertexes, matr, local_degrees, x))
                print("\tНова множина: ", x)
                print("\tПотужність множини становить:", len(x))
                if len(x) in power_of_subgraphs_2:
                    # print("in")
                    Δ.append(Cutting_Factor(x, matr, local_degrees, vertexes))
                    print("\tКоефіцієнт отриманого розрізання:", Δ[-1], "\n")
                    power_of_subgraphs_2.remove(len(x))
                vertex_min_number = x[-1]
                # print(vertex_min_number)
            final_graph_list.append(x)
            print("\t\tПоточний список підграфів:", final_graph_list, "\n")
            power_of_subgraphs.remove(len(x))
            # print(power_of_subgraphs)
            i = 0
            while i < len(vertexes):
                for j in range(len(x)):
                    # print(x, j, x[j])
                    # print(vertexes, i, vertexes[i], "\n")
                    if x[j] == vertexes[i]:
                        vertexes.remove(vertexes[i])
                        matr = New_Matrix(matr, i)
                        # print(vertexes)
                        # for k in range(len(matr)):
                        #         print(matr[k])
                        i -= 1
                    # print()
                i += 1
        if len(power_of_subgraphs) > 1:
            Print_Matrix(matr, vertexes, power_of_subgraphs, cant_be_min, final_graph_list)
        else:
            x = []
            for i in range(len(vertexes)):
                x.append(vertexes[i])
            # print(x)
            final_graph_list.append(x)
            print("\t\tКінцевий список підграфів:", final_graph_list, "\n")

        # vertex_numbers = What_To_Do_With_Subgraphs(power_of_subgraphs, vertex_numbers, final_graph_list)
        # vertex_numbers.sort(reverse=True)
        # if len(power_of_subgraphs) > 1:
        #     for i in vertex_numbers:
        #         vertexes.remove(i)
        #         matr = New_Matrix(matr, i)
        #     Print_Matrix(matr, vertexes, power_of_subgraphs, cant_be_min, final_graph_list)
        # else:
        #     for i in vertex_numbers:
        #         vertexes.remove(i)
        #     What_To_Do_With_Subgraphs(power_of_subgraphs, vertexes, final_graph_list)

def Min_Vertex(min, local_degrees, width, vertexes, cant_be_min):
    vertex_min_number = vertexes[0]
    for i in range(width):
        if vertexes[i] not in cant_be_min and min > local_degrees[i]:
            min = local_degrees[i]
            vertex_min_number = vertexes[i]
    print("\tВершина з мінімальним локальним ступенем: ", vertex_min_number)
    return vertex_min_number

def New_Plural (matr, vertex_min_number, vertexes):
    vertex_numbers = []
    # vertex_numbers.append(vertex_min_number)
    count = 0
    # if vertex_min_number > 1:
    #     vertex_min_number -= 1
    for i in matr[vertexes.index(vertex_min_number)]:
        count += 1
        if i > 0:
            vertex_numbers.append(vertexes[count-1])
    print("\tМножина вершин суміжних з початковою вершиною ", vertex_min_number, ":", vertex_numbers)
    return vertex_numbers

def Connectivity_Factor(vertex_min_number, set_combination, vertexes, matr, local_degrees, x):
    σ = []
    i = 0
    # print(set_combination)
    while i < len(set_combination):
        # print(set_combination, x)
        if vertex_min_number != set_combination[i] and set_combination[i] not in x:
            ρ = local_degrees[vertexes.index(set_combination[i])]
            z = 0
            for j in range(len(set_combination)):
                # print(i, j)
                # print(set_combination[j])
                # print("matr[", vertexes.index(set_combination[i]), "][", vertexes.index(set_combination[j]), "]:", matr[vertexes.index(set_combination[i])][vertexes.index(set_combination[j])])
                if matr[vertexes.index(set_combination[i])][vertexes.index(set_combination[j])] != 0:
                    z += matr[vertexes.index(set_combination[i])][vertexes.index(set_combination[j])]
                # if matr[set_combination[i]-1][set_combination[j]-1] != 0:
                #     z += matr[set_combination[i]-1][set_combination[j]-1]
            σ.append(ρ - z)
            i += 1
        elif vertex_min_number == set_combination[i] or set_combination[i] in x:
            set_combination.remove(set_combination[i])

    min = σ[0]
    minp = set_combination[0]
    for i in range(len(σ)):
        if min > σ[i]:
            min = σ[i]
            minp = set_combination[i]

    return minp

def Cutting_Factor(x, matr, local_degrees, vertexes):
    L = 0
    K = 0
    for i in range(len(x)):
        z = 0
        for j in range(len(x)):
            if matr[vertexes.index(x[i])][vertexes.index(x[j])] != 0:
                z += matr[vertexes.index(x[i])][vertexes.index(x[j])]
                # print("matr[", x[i], "][", x[j], "]:", matr[x[i] - 1][x[j] - 1])
        L += z
        # print(L)
    L /= 2
    # print(L)
    for i in range(len(local_degrees)):
        for j in range(len(x)):
            if i == vertexes.index(x[j]):
                K += local_degrees[i]
    K -= L
    # print(K)
    Δ = L/K
    # print(round(Δ, 2))
    return round(Δ, 2)

def New_Matrix(matr, idx):
    _ = matr.pop(idx)
    rows = len(matr)
    for j in range(rows):
        _ = matr[j].pop(idx)
    return matr

###########################
Initial_Conditions([])