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
# tính ngày trong năm có 365 ngày 
# tạo dữ liệu tháng 
month_data= [31,28,31,30,31,30,31,31,30,31,30,31]
def count_day(n, month, month_data):
    for i in range(len(month_data)):
        if i+1 == month:
            num_day= sum(month_data[0:i]) + n
    return num_day # trả hàm về giá trị đệ tận dụng kết quả 

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
    gamma= math.radians(360*(n-1)/365)
    LSM= 15*TZ
    ET= 2.2918 * (0.0075 + 0.1868*math.cos(gamma) - 3.2077*math.sin(gamma) - 1.4615*math.cos(2*gamma) - 4.089*math.sin(2*gamma)) # hàm lượng giác mặc đinh tính theo giá trị rad
    AST= LST + ET/60 + (LON-LSM)/15
    return AST

# góc được tạo bởi tia tới của mặt trời và đường xích đạo 
def declination(n):
    sigma= 23.45*math.sin(360*math.pi/180*(n + 284)/365)
    return sigma

# tính góc cao mặt trời 
'''
| L: vĩ độ thực tế [oN] |
'''
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
def air_mass(beta_o):
    beta= math.radians(beta_o)
    m= 1/(math.sin(beta) + 0.50572*(6.07995 + beta_o)**(-1.6364))
    return m 

print(air_mass(76.80))