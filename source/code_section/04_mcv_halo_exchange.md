# MCV影像区交换功能

影像区交换功能是MCV并行软件框架核心功能。MCV模式采用空间区域分解的MPI并行实现，带来所谓的影像区（halo）更新需求。为了保证每个进程使用的影像区内数值与邻居进程计算区域一致，必须在计算区域值发生变化后进行影像区更新。

MCV影像区交换功能能够支持全球立方球网格和区域经纬度网格。立方球网格每个面内部的影像区更新与经纬度网格类似，除此之外，立方球网格还需要处理面边界插值和面重叠边一致性需求。

MCV模式并行软件框架开发了以下接口满足不同的影像区交换功能。

| 接口程序                | 用途              |
|:--------------------|:----------------|
| bch_scalar          | 单个标量影像区交换       |
| bch_vector          | 水平向量影像区交换       |
| bch                 | 动力预报变量影像区交换     |
| bch_moist           | 示踪物变量影像区交换      |
| bcorrection         | 动力预报变量面重叠区一致性修正 |
| bcorrection_moist   | 示踪物面重叠区一致性修正    |
| exchange_patch_halo | 立方球面边界影像区更新     |  

## 接口说明

### bch_scalar 

- 功能：单个标量类型变量的影像区交换。对于MCV全球模式，除了常规影像区更新，包括立方球面边界影像区插值更新处理。

- 实现接口

```fortran
subroutine bch_scalar(qt,gl,jm,coord,qh)

type(gloc),intent(in) :: gl
type(jame),intent(in) :: jm
type(cord),intent(in) :: coord 
real,dimension(gp%kms:gp%kme,gp%ims:gp%ime,gp%jms:gp%jme,gp%fms:gp%fme) :: qt
type(cell),target,optional,intent(in)  :: qh
```

参数含义： 

  - gl: 立方球网格面边界halo点信息
  - jm: 坐标雅可比和度量项
  - coord: 计算网格坐标
  - qt: 标量类型的影像区交换变量
  - qh: 可选参数，交换变量对应的参考廓线平均态，如果参数存在表示，表示热力学变量在面边界插值前需要先扣除平均态，使用扰动态进行处理

- 示例：

```fortran
call bch_scalar(qs%pv,gl,jm,coord)
```

### bch_vector 

- 功能：水平矢量类型变量的影像区交换。对于MCV全球模式，除了常规影像区更新，包括立方球面边界影像区插值更新处理。

- 实现接口

```fortran
subroutine bch_vector(qt,gl,jm,coord,using_buffer)

type(gloc),intent(in) :: gl
type(jame),intent(in) :: jm
type(cord),intent(in) :: coord 
type(cell),dimension(2),target,intent(inout)  :: qt 
logical,intent(in), optional :: using_buffer
```

参数含义：  

 - gl: 立方球网格面边界halo点信息
  - jm: 坐标雅可比和度量项
  - coord: 计算网格坐标
  - qt: 水平矢量分量影像区交换变量，cell派生类型数据
  - using_buffer: 可选参数，是否使用内部注册缓冲进行交换。如存在且为`.true.`，表示qt变量没有经过C-Coupler注册，使用内部注册变量bch_buffer进行影像区交换 

- 示例：

```fortran
call bch_vector(qvec(2:3),gl,jm,coord,using_buffer=.true.)
```

### bch 

- 功能：多个变量打包影像区交换。对于MCV全球模式，除了常规影像区更新，包括立方球面边界影像区插值更新处理。 

- 实现接口 

```fortran
subroutine bch(qt,gl,jm,coord,nvar,using_buffer,disable_patch_bound,var_type,qh)

integer,intent(in)    :: nvar 
type(gloc),intent(in) :: gl
type(jame),intent(in) :: jm
type(cord),intent(in) :: coord 
type(cell),dimension(nvar),target,intent(inout)  :: qt 
logical,intent(in), optional :: using_buffer 
logical,intent(in), optional :: disable_patch_bound 
integer,intent(in), optional :: var_type 
type(cell),dimension(nvar),target,optional,intent(in)  :: qh
```

参数含义：

  - nvar: 影像区交换变量数目
  - gl: 立方球网格面边界halo点信息
  - jm: 坐标雅可比和度量项
  - coord: 计算网格坐标
  - qt: 影像区交换变量，cell派生类型数据
  - using_buffer: 可选参数，是否使用内部注册缓冲进行交换。如存在且为`.true.`，表示qt变量没有经过C-Coupler注册，使用内部注册变量bch_buffer进行影像区交换 
  - disable_patch_bound: 可选参数，如存在且为`.true.`，表示不对立方球面边界进行插值处理
  - var_type: 可选参数，如果参数存在，当值为1时，表示交换变量中第2和3个变量为矢量分量，其它为标量；当值为2时，表示所有交换变量为标量类型
  - qh: 可选参数，参考廓线平均态，如果参数存在表示，表示热力学变量在面边界插值前需要先扣除平均态，使用绕动态进行处理

- 示例

```fortran
call bch(qt,gl,jm,coord,nvar,qh=qh) 

call bch(diffq,gl,jm,coord,nvar,using_buffer=.true.,var_type=2)
```

### bch_moist 

- 功能：多示踪物类型变量打包影像区交换。对于MCV全球模式，除了常规影像区更新，包括立方球面边界影像区插值更新处理。 

- 实现接口 

```fortran
subroutine bch_moist(qt,q,gl,jm,coord,nvar,ntracer)

integer,intent(in)    :: nvar 
integer,intent(in)    :: ntracer
type(gloc),intent(in) :: gl
type(jame),intent(in) :: jm
type(cord),intent(in) :: coord 
type(cell),dimension(nvar),intent(in)       :: q
type(cell),dimension(ntracer),intent(inout)  :: qt
```

参数含义：

  - nvar: 动力预报变量数目
  - ntracer: 示踪物类型影像区交换变量数目
  - gl: 立方球网格面边界halo点信息
  - jm: 坐标雅可比和度量项
  - coord: 计算网格坐标
  - qt: 示踪物类型影像区交换变量，cell派生类型数据
  - q: 动力预报变量，辅助示踪物变量进行影像区交换处理

- 示例

```fortran
call bch_moist(qmoist,qt,gl,jm,coord,nvar,ntracer)
```

### bcorrection 

- 功能：用于MCV全球立方球网格动力预报变量的面重叠边一致性处理。

- 实现接口

```fortran
subroutine bcorrection(qvar,coord,nvar)

integer,intent(in)       :: nvar 
type(cord),intent(in)    :: coord 
type(cell),dimension(nvar),intent(inout)    :: qvar
```

参数含义： 

  - nvar: 动力预报变量数目
  - coord: 计算网格坐标
  - qvar: 面重叠边一致性处理的预报变量 

- 示例

```fortran
call bcorrection(rqht,coord,nvar)
```


### bcorrectio_moist 

- 功能：用于MCV全球立方球网格示踪物类型变量的面重叠边一致性处理。

- 实现接口

```fortran
subroutine bcorrection_moist(qvar,coord,nvar,min_max_label)

integer,intent(in)       :: nvar 
type(cord),intent(in)    :: coord 
type(cell),dimension(nvar),intent(inout)    :: qvar
integer,intent(in),optional  :: min_max_label
```

参数含义： 

  - nvar:示踪物变量数目
  - coord: 计算网格坐标
  - qvar: 面重叠边一致性处理的示踪物变量
  - min_max_label: 可选参数，缺省面重叠边一致性处理采用代数平均操作，如参数存在，当值为1时表示采用绝对值最小一致性操作；当值为2时表示采用绝对值最大一致性操作。

- 示例

```fortran
call bcorrection_moist(qmt,coord,ntracer) 

call bcorrection_moist(qmt,coord,ntracer,1)
```

### exchange_patch_halo 

- 功能：立方球面边界角落影像区更新。

- 实现接口

```fortran
subroutine exchange_patch_halo(qt,nvar)

integer,intent(in)    :: nvar 
type(cell),dimension(nvar),target,intent(inout)  :: qt
```

参数含义： 

  - nvar: 变量数目
  - qt: 立方球面边界角落影像区更新变量。

- 示例

```fortran
call exchange_patch_halo(qvarp,nvar)
```

