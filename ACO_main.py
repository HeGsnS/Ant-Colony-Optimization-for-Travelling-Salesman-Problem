#!

import random
import numpy

nectar_upd_func = lambda rho, nectar_old, nectar_ant: (1 - rho) * nectar_old + sum(nectar_ant)
o_dis_func = lambda x, y: (x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2

def nectar_ant_upd(L_ant, Q):
    nectar_ant = [Q/x for x in L_ant]
    return nectar_ant

def nectar_path_upd(rho, nectar_path, nector_ant, loc1_ant, loc2_ant):
    Num_city = len(nectar_path)
    nectar_path_nxt = [[0 for idx1 in range(Num_city)] \
                            for idx2 in range(Num_city)]
    for idx1 in range(Num_city):
        for idx2 in range(Num_city):
            nector_ant_current = [nector_ant[idx3] for idx3 in range(len(nector_ant)) \
                            if loc1_ant[idx3] == idx1 and loc2_ant[idx3] == idx2]
            nectar_path_nxt[idx1][idx2] = nectar_upd_func(rho, nectar_path[idx1][idx2], \
                                                        nector_ant_current)
    return nectar_path_nxt

def tran_pro_upd(nectar_path, alpha, eta, beta):
    Num_city = len(nectar_path)
    trans_pro = [[0 for idx1 in range(Num_city)] for idx2 in range(Num_city)]
    for idx1 in range(Num_city):
        nectar_sum = sum([nectar_path[idx1][idx3]**alpha * eta[idx1][idx3]**beta \
                          for idx3 in range(Num_city)])
        for idx2 in range(Num_city):
            trans_pro[idx1][idx2] = nectar_path[idx1][idx2]**alpha * eta[idx1][idx2]**beta \
                                    /nectar_sum
    # print(trans_pro)
    return trans_pro

def ant_simulation_once(Num_ant, loc_ant, L_ant, trans_pro, adj_matrix, travel_route):
    # print(travel_route)
    Num_ant = len(loc_ant)
    Num_city = len(adj_matrix)
    loc_ant_nxt = []
    L_ant_nxt = []
    for idx1 in range(Num_ant):
        city_idx = loc_ant[idx1]
        ctrans_pro = trans_pro[city_idx]
        finished_travel = [travel_route[idx2][idx1] for idx2 in range(len(travel_route))]
        trans_pro_unfinishd = [ctrans_pro[idx] for idx in range(Num_city) \
                                                if idx not in finished_travel]
        # print(trans_pro_unfinishd)
        trans_pro_unfinishd_normal = [x/sum(trans_pro_unfinishd) for x in trans_pro_unfinishd]
        city_choose_buf = [idx for idx in range(Num_city) \
                                if idx not in finished_travel]

        cloc_ant_nxt = numpy.random.choice(city_choose_buf, p=trans_pro_unfinishd_normal)
        cL_ant_nxt = L_ant[idx1] + adj_matrix[city_idx][cloc_ant_nxt]
        loc_ant_nxt.append(cloc_ant_nxt)
        L_ant_nxt.append(cL_ant_nxt)

    return loc_ant_nxt, L_ant_nxt


def main():
    Num_city = 20
    corrd = [[random.uniform(0,100), random.uniform(0,100)] for idx in range(Num_city)]
    adj_matrix = [[ o_dis_func(corrd[idx1], corrd[idx2]) + 10  \
        for idx1 in range(Num_city)] for idx2 in range(Num_city)]
    Num_ant = 100
    nectar_init = 100
    rho = 0.2
    alpha = 0.9
    beta = 0.1
    # nectar_ant = [nectar_init for idx in range(Num_ant)]
    trans_pro = [[1/Num_city for idx1 in range(Num_city)] \
                        for idx2 in range(Num_city)]
    L_ant = [0 for idx in range(Num_ant)]
    nectar_path = [[10 for idx1 in range(Num_city)] for idx2 in range(Num_city)]
    loc_ant = [random.randint(0, Num_city-1) for idx in range(Num_ant)]
    eta = [[1/d for d in r] for r in adj_matrix]

    iter_THD = 1000
    travel_route = [loc_ant]
    for iter_idx in range(iter_THD):
        travel_route = [loc_ant]
        # print(travel_route)
        for travel_time in range(Num_city - 1):
            if travel_time > 0:
                nectar_ant = nectar_ant_upd(L_ant, nectar_init)
                nectar_path = nectar_path_upd(rho, nectar_path, nectar_ant, \
                                    travel_route[-2], travel_route[-1])

                trans_pro = tran_pro_upd(nectar_path, alpha, eta, beta)
            loc_ant, L_ant = ant_simulation_once(Num_ant, loc_ant, L_ant, \
                                                 trans_pro, adj_matrix, travel_route)
            travel_route.append(loc_ant)
            # print(loc_ant)
    route_ant = [[travel_route[idx2][idx1] for idx2 in range(len(travel_route))] \
                 for idx1 in range(Num_ant)]

    print(route_ant)

    return


if __name__ == '__main__':
    main()
