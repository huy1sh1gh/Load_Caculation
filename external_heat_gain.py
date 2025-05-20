# thư viện nền 
import math 
# Nhiệt truyền qua kết cấu bao che 
'''
| Sol-Air Temperature: nhiệt độ không khí ngoài trời giả định |
| mà nếu chỉ có truyền nhiệt đối lưu giữa không khí ngoài và  |
| bề mặt, nó sẽ tạo ra cung một dòng nhiệt truyền qua kết cấu |
| như khí xét đến:                                            |
| * Bức xạ qua mặt trời.                                      |
| * Bức xạ dài.                                               |
| * Truyền nhiệt đối lưu với không khí.                       |
| Nói đơn giản: Nó gom tất cả các ảnh hưởng nhiệt bên ngoài   |
| vào một nhiệt độ suy nhất để dễ tính toán hơn.              |
| Trích trang 494 - Ashrae Hanbook 2017                       |
'''

# lưu ý cách xây dựng cơ sở dữ liệu cho tau_b,d
tau= [[0.448, 2.157], 
      [0.513, 2.078],
      [0.551, 2.012],
      [0.530, 2.093],
      [0.461, 2.335],
      [0.452, 2.382],
      [0.452, 2.372],
      [0.455, 2.356],
      [0.460, 2.331],
      [0.495, 2.219],
      [0.461, 2.314],
      [0.461, 2.276]
      ]

# tính ngày trong năm có 365 ngày 
def count_day(day, month):
    month_data= [31,28,31,30,31,30,31,31,30,31,30,31]
    for i in range(len(month_data)):
        if i+1 == month:
            n= sum(month_data[0:i]) + day
    return n # trả hàm về giá trị để tận dụng kết quả 

# tính bức xạ mặt trời ngoài khí quyển trái đất 
def RadFlux_o(n):
    E_o= 1367*(1+0.033*math.cos(360*math.pi/180*(n-3)/365))
    return E_o

#  tính giờ mặt trời biểu kiến 
'''
| n  : số thứ tự ngày trong năm (1-365) |
| TZ : múi giờ theo khu vực             |
| LST: giờ đồng hồ địa phương           |
| LSM: kinh độ kinh tuyến chuẩn [oE]    |
| LON: kinh độ địa điểm thực tế [oE]    |
| ET : phương trình thời gian           |
'''
def A_SolarTime(n, LST, LON, TZ):
    Gamma= math.radians(360*(n-1)/365)
    LSM= 15*TZ
    ET= 2.2918 * (0.0075 + 0.1868*math.cos(Gamma) - 3.2077*math.sin(Gamma) - 1.4615*math.cos(2*Gamma) - 4.089*math.sin(2*Gamma)) # công thức Iqbal 1983 
    AST= LST + ET/60 + (LON-LSM)/15
    return AST # phụ thuộc thời gian trong ngày 

# góc được tạo bởi tia tới của mặt trời và đường xích đạo 
def declination_angle(n):
    sigma= 23.45*math.sin(360*math.pi/180*(n + 284)/365)
    return sigma

# tính góc cao mặt trời 
'''
| L: vĩ độ thực tế [oN] |
'''
# khi beta < 0 mặt trời đang lặn khi đó bức xạ mặt trời đối với mặt phẳng ngang là không có
def altitude_angle(AST, L, sigma):
    H= 15*(AST-12)
    if H== 0:
        beta= (90 - abs(L - sigma))
    else:
        beta= math.degrees(math.asin((math.cos(L*math.pi/180)*math.cos(sigma*math.pi/180)*math.cos(H*math.pi/180) + math.sin(L*math.pi/180)*math.sin(sigma*math.pi/180)))) 
    return beta

# tính góc phương vị 
def azimuth_angle(AST, L, sigma, beta):
    H= 15*(AST-12)
    sin_phi= math.sin(H*math.pi/180)*math.cos(sigma*math.pi/180)/math.cos(beta*math.pi/180)
    cos_phi= (math.cos(H*math.pi/180)*math.cos(sigma*math.pi/180)*math.sin(L*math.pi/180)-math.sin(sigma*math.pi/180)*math.cos(L))/math.cos(beta*math.pi/180)
    phi= math.degrees(math.asin(sin_phi))
    return phi

# tính tỉ lệ khối lượng không khí 
def air_mass(beta):
    beta_r= math.radians(beta)
    m= 1/(math.sin(beta_r) + 0.50572*(6.07995 + beta)**(-1.6364))
    return m 

# tính bức xạ mặt trời đối với mặt phẳng ngang
def G_SolRad(month, tau, m, E_o):
    for i in range(len(tau)):
        if i + 1 == month:
            tau_b= tau[i][0]
            tau_d= tau[i][1]
            ab= 1.454 - 0.406*tau_b - 0.268*tau_d + 0.021*tau_b*tau_d
            ad= 0.507 + 0.205*tau_b - 0.080*tau_d - 0.190*tau_b*tau_d
            E_b= E_o*math.exp(-tau_b*m**ab)
            E_d= E_o*math.exp(-tau_d*m**ad)
            E_bd= [E_b, E_d]
    return E_bd

# tính bức xạ mặt trơi đối với tường, mái nghiêng, hoặc cửa sổ 
# tính góc phương vị tương đối của mặt trời và bề mặt 
def S_SolAzim(phi, psi):
    gamma= phi - psi 
    return gamma

# tính góc giữa tia nắng và pháp tuyến bề mặt 
def incidence_angle(beta, gamma, Sigma):
    beta_r= math.radians(beta)
    gamma_r= math.radians(gamma)
    sigma_r= math.radians(Sigma)
    if Sigma== 90:
        theta= math.degrees(math.acos(math.cos(beta_r)*math.cos(gamma_r)))
    elif Sigma== 0:
        theta= 90 - beta
    else: 
        theta= math.degrees(math.acos(math.cos(beta_r)*math.cos(gamma_r)*math.sin(sigma_r) + math.sin(beta_r)*math.cos(sigma_r)))
    return theta

# tính tổng bức xạ mặt trời chiếu lên bề mặt
'''
Trích trang 310 -  Ashrae Hanbook 2017 
'''
def S_SolRad(E_bd, theta, Sigma, beta, rho_g):
    E_b= E_bd[0]
    E_d= E_bd[1]
    theta_r= math.radians(theta)
    Sigma_r= math.radians(Sigma)
    beta_r= math.radians(beta)
    # tính bức xạ trực tiếp lên bề mặt
    if math.cos(theta_r) > 0:
        E_tb= E_b*math.cos(theta_r)
    else: 
        E_tb= 0
    # tính thành phần khuếch tán lên bề mặt
    Y= max(0.45, 0.55 + 0.437*math.cos(theta_r) + 0.313*math.cos(theta_r)**2)
    if Sigma <= 90:
        E_td= E_d*(Y*math.sin(Sigma_r) + math.cos(Sigma_r))
    elif Sigma_r > 90: 
        E_td= E_d*Y*math.sin(Sigma_r)
    #tính thành phần phản xạ từ mặt đất 
    E_tr= (E_b*math.sin(beta_r) + E_d)*rho_g*(1 + math.cos(beta_r))/2
    # tính tổng bức xạ lên bề mặt
    E_t= [E_tb, E_td, E_tr]
    return E_t

# tính toán bức xạ mặt trời so với mặt ngang trong ngày từ 0h tới 23h
def SolRad_ts(day, month, LON, L, TZ, psi, Sigma, rho_g):
    # tính bức xạ mặt trời lên mặt ngang
    n= count_day(day, month)
    E_o= RadFlux_o(n)
    sigma= declination_angle(n)
    AST_ts=     [A_SolarTime(n, i, LON, TZ) for i in range(24)]
    beta_ts=    [altitude_angle(i, L, sigma) for i in AST_ts]
    comb_1=     [[i, j] for i, j in zip(AST_ts, beta_ts)]
    phi_ts=     [azimuth_angle(i[0], L, sigma, i[1]) for i in comb_1]
    m_ts=       [air_mass(i) for i in beta_ts]
    mm_ts=      [0 if isinstance(i, complex) else i for i in m_ts]
    Ebd_ts=     [[0, 0] if i ==0 else G_SolRad(5, tau, i, E_o) for i in mm_ts]
    # tính bức xạ mặt trời lên các mặt đứng, nghiêng
    gamma_ts=   [i - psi for i in phi_ts]
    comb_2=     [[i, j] for i, j in zip(beta_ts, gamma_ts)]
    theta_ts=   [incidence_angle(i[0], i[1], Sigma) for i in comb_2]
    comb_3=     [[i, j, x] for i, j, x in zip(Ebd_ts, theta_ts, beta_ts)]
    Et_ts=      [S_SolRad(i[0], i[1], Sigma, i[2], rho_g) for i in comb_3]
    E_overall=  [Ebd_ts, Et_ts]
    return E_overall

E_overall= SolRad_ts(26, 5, 106.6803, 10.7656, 7, -15, 90, 0.2)
for i in E_overall[1]:
    print(i)
# print(AST_list)
# print(beta_list)
# print(phi_list)
# print(mm_list)

