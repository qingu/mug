# MCV诊断工具

## 物理场最大最小值打印

MCV模式提供`resultmax`和`resultmin`程序打印七个物理场预报区域最大、最小值以及所在网格位置(faceid,i,j,k)。

七个物理场分别是:

- r 干空气密度
- u 球坐标东西向风速
- v 球坐标南北向风速
- w 垂直速度 
- t 位温 
- p 气压
- c 声速

目前在每个积分步动力过程计算后调用诊断程序打印极值，用于诊断模式状态的合理性。

程序调用示例：

```fortran
call resultmax(q,qh,gl,jm,coord,5)
call resultmin(q,qh,gl,jm,coord,5)
```

输出LOG示例：

```
-------------- max info ------------------
r     1.50928005913277      at           6          34          54           1
u     109.921031671560      at           6          85          70          60
v     64.4290566992579      at           6          88          68          29
w     1.26273419784404      at           4          25          78          34
t     1305.97690163983      at           6          48          66          60
p     103292.408967159      at           3          88           2           1
c     358.119149469112      at           2           6          83           1
-------------- min info ------------------
r    3.710950064551646E-003 at           6          53          56          60
u    -46.1393560662881      at           6          34          35          28
v    -64.1574987727892      at           6          68          85          29
w   -0.578041169498615      at           6          86          42          55
t     232.507531969476      at           6          34          54           1
p     239.084112118258      at           6          48          51          60
c     266.156402053699      at           6          43          48          44
```


