# 预处理模块MPS
## 简要介绍 

Mcv Preprocess Systerm(MPS)是为新一代MCV模式开发的预处理系统，其功能即为MCV模式提供其所必需的初始场、边界条件（用于有限区域运行）以及物理过程静态资料等信息，以确保模式能够获得正确的数据输入，从而得到合理的预报结果。为了模式冷启动的进行，首先必须通过解码前端模式预报或再分析数据得到可以直接被MPS读取的数据格式，同时需要根据所给出的参数设置生成模式网格以及地形等相关数据；而后需要将解码后的气象数据插值到模式网格，并根据需要进行缺失大气变量的补充。

MPS系统分为四个部分，分别为grib数据解码模块ungrib，地形及静态资料生成模块gengeo，水平插值模块interpmet以及初始场生成模块realdata。

## 安装MPS

```bash
# 加载modulefile会自动设置以下环境变量
# export JASPER=/path/to/install/jasper
# export LAPACK_ROOT=/path/to/install/lapack
# export NETCDF=/path/to/install/netcdf   
$ tar xzvf MCV_PUBLIC-v1.0.tar.gz
$ cd MCV_PUBLIC-v1.0/MPS
$ mkdir build
$ cd build
$ FC=ifort CC=icc cmake ..
$ make -j 8
$ cd ../run
$ ln -s ../build/*.exe .
```

## 运行MPS

```bash
$ cd MPS/run

# 编辑namelist.input文件

# 链接MPS所需静态数据到运行目录下
$ ln -sf $FIX_DATA/source_data .

# 执行gengeo程序生成MCV网格和地形文件mcv_geog.nc
$ ./gengeo.exe

# 链接GRIB文件，生成GRIBFILE.XXX文件
# NCEP GFS测试数据示例
$ ./ link_grib.csh $FIX_DATA/source_data/met_data/NCEP_GFS/2022081000/gfs.t00z.pgrb2.0p50.f000

# 解码GRIB文件，生成FILE:YYYY-MM-DD_HH的二进制文件
$ ./ungrib.exe

# 进行变量场水平插值，生成mcv_met_YYYYMMDDhhmmss.nc
$ ./interpmet.exe

# 进行变量场垂向插值，生成最终MCV驱动场mcv_input_$YYYYMMDDhhmmss.nc（区域版本同时生成侧边界条件数据）
$ ./realdata.exe
```

namelist.input参数说明见附录A。



