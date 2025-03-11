# 预处理模块MPS
## 简要介绍 

Mcv Preprocess Systerm(MPS)是为新一代MCV模式开发的预处理系统，其功能即为MCV模式提供其所必需的初始场、边界条件（用于有限区域运行）以及物理过程静态资料等信息，以确保模式能够获得正确的数据输入，从而得到合理的预报结果。为了模式冷启动的进行，首先必须通过解码前端模式预报或再分析数据得到可以直接被MPS读取的数据格式，同时需要根据所给出的参数设置生成模式网格以及地形等相关数据；而后需要将解码后的气象数据插值到模式网格，并根据需要进行缺失大气变量的补充。

MPS系统分为四个部分，分别为grib数据解码模块ungrib，地形及静态资料生成模块gengeo，水平插值模块interpmet以及初始场生成模块realdata。

## 安装MPS

```bash
# 气象局局超算加载modulefile会自动设置以下环境变量
# export JASPER=/path/to/install/jasper
# export LAPACK_ROOT=/path/to/install/lapack
# export NETCDF=/path/to/install/netcdf   

$ cd MPS
$ mkdir build
$ cd build
$ FC=ifort CC=icc cmake ..
$ make -j 8
$ cd ../run
$ ln -sf ../build/*.exe .
```

## 运行MPS

```bash
# 进入MPS根目录
$ cd MPS

# 链接MPS所需静态数据到运行目录下
$ ln -sf $FIX_DATA/../source_data .

# 进入MPS运行目录
$ cd run

# 编辑namelist.input文件

# 执行gengeo程序生成MCV网格和地形文件mcv_geog.nc
$ ./gengeo.exe

# 链接GRIB文件，生成GRIBFILE.XXX文件
# NCEP GFS测试数据示例
$ ./link_grib.csh $FIX_DATA/../source_data/met_data/NCEP_GFS/2022081000/gfs.t00z.pgrb2.0p50.f000

# 解码GRIB文件，生成FILE:YYYY-MM-DD_HH的二进制文件
$ ./ungrib.exe

# 进行变量场水平插值，生成mcv_met_YYYYMMDDhhmmss.nc
$ ./interpmet.exe

# 进行变量场垂向插值，生成最终MCV驱动场mcv_input_$YYYYMMDDhhmmss.nc（区域版本同时生成侧边界条件数据）
$ ./realdata.exe
```

namelist.input参数说明见附录A。

通常高性能计算机登录节点不允许运行应用程序，请参考以下SBATCH脚本提交到计算节点。

```bash
#!/bin/bash
# mps.sbatch

#SBATCH -J MCV
#SBATCH --comment=MCV
#SBATCH --wckey=xxxx
#SBATCH -p normal
#SBATCH -n 1
#SBATCH --ntasks-per-node=1
#SBATCH -c 64
#SBATCH -o mps_%j.out
#SBATCH -e mps_%j.err


ulimit -s unlimited
ulimit -c unlimited

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

./gengeo.exe
./ungrib.exe
./interpmet.exe
./realdata.exe
```

### 高（74km）/低（36km）顶版本切换
修改namelist.input中四个参数可以灵活切换垂直层顶和层数生成MCV初始场

- nz
- z_max
- vgrid_file
- vgrid_deriv_file

| 版本 | nz     |   z_max  | vgrid_file | vgrid_deriv_file |
|------|--------|-----------|------------|-----------------|
| 高顶74km L137 | 137 | 74000 | ./zbar_ML_74km_L137.dat | ./dzbardz_ML_74km_L137.dat |
| 低顶36km L60 | 60 | 36000 | ./zbar_ML_36km_L60.dat | ./dzbardz_ML_36km_L60.dat |

