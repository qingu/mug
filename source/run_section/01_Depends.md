# 准备工作
## 依赖环境准备

| 依赖库 | 环境变量设置 | 说明 |
|:------:|:---------------:|:-----:|
| netCDF | NETCDF      | 支持netCDF-4/HDF格式 |
| Jasper | JASPER 或 JASPER_ROOT | 
| PNG    | PNG 或 PNG_ROOT |   |
| LAPACK | LAPACK_ROOT |   |
| PnetCDF| PNETCDF     | 版本不低于1.3.0 |
| NCEPLIBS | NCEPLIBS_DIR |  |
| CMake |       | 版本不低于3.0.0 |

如果用户使用中国气象局新一代高性能计算机平台，依赖环境设置建议如下：

```bash
# vi ~/.bashrc
module load netcdf_no_pnetcdf/4.8.1/intel
module load jasper/1.900.19/intel 
module load libpng/1.6.39/intel
module load cmake/3.25.3/gnu
module load pnetcdf/1.12.3/intel

export PNETCDF=/g1/app/mathlib/pnetcdf/1.12.3/intel
export WCKEY=xxx-xx-xx # CMA HPC用户根据分配的wckey信息设置，其它环境不需要设置

if [[ $HOSTNAME == login_a* || $HOSTNAME == login_b* ]]; then
  export NCEPLIBS_DIR=/g5/jiangqg/share/NCEPlibs 
  export FIX_DATA=/g5/jiangqg/share/FIX_DATA
elif [[ $HOSTNAME == login_c* ]]; then
  export NCEPLIBS_DIR=/g4/jiangqg/share/NCEPlibs 
  export FIX_DATA=/g4/jiangqg/share/FIX_DATA
fi
```

## MCV静态数据及源代码包准备

- FIX_DATA

MCV模式运行所需的参考廓线、物理静态数据等。

在中国气象局新一代高性能计算机上可以直接使用公共静态数据，设置环境变量`FIX_DATA`.
（后面以$FIX_DATA指代静态数据目录）。

- MCV_PUBLIC-v1.0.tar.gz

MCV源代码包。

