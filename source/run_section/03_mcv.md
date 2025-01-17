# MCV主模式 

## 简要介绍

在准备好模式积分所需的初始场（及区域模式边界场）数据后，下一步进入MCV模式积分预报环节。MCV非静力大气模式是基于球面曲线坐标系，采用多矩约束有限体积方法（Multi-moment Constrained Finite Volume Method，简称MCV）研发的高精度、数值守恒的区域/全球一体化完全可压缩的多矩非静力大气模式。多矩非静力大气模式动力框架的通量型控制方程建立在曲线坐标系下，可以通过曲线坐标系下的度量项切换，实现区域/全球球面数值网格一体化设计。当前全球模式采用球面立方球网格，区域模式采用传统经纬度网格。

## 安装MCV模式

### 简单安装方法

MCV模式默认提供全球模式在中国气象局新一代高性能计算平台环境编译运行配置信息。默认配置信息为：

- 基础编译器（Intel icc/ifort）
- MPI库（Intel MPI）
- 作业调度器（Slurm）
- 计算节点信息（每个节点64核）
- NETCDF库路径

如果用户在该平台运行MCV，可以使用以下简便安装方法。

```bash
$ cd CCPL_PMCV/Experiments/PMCV
$ source setenv.sh
$ ./configure
$ ./clean all
$ ./compile
```

安装成功标志除了终端输出的Compile Completed信息外，在Experiments/PMCV/run/atm/MCV/exe目录下会生成可执行程序MCV。

### 详细安装方法

如果用户在其它计算平台运行，计算环境与中国气象局新一代高性能计算平台环境有差异，需要按照以下步骤修改配置文件。

- 编译器及库信息

修改配置文件`CCPL_PMCV/Experiments/PMCV/config/common/machine/generic_linux/common_compiler.generic_linux.cfg`中相应参数。

- 计算节点及作业调度器信息

修改目录`CCPL_PMCV/Experiments/PMCV/config/common/machine/generic_linux`中配置文件`env.generic_linux`，并以`submit.sbatch.generic_linux`为模板创建本平台作业调度脚本，比如使用PBS作业调度器，创建一个名为`submit.bsub.generic_linux`的脚本。

修改好配置文件文件，首先执行configure脚本使配置生效，然后compile编译安装MCV。

### 区域模式安装方法

在配置文件`CCPL_PMCV/Experiments/PMCV/config/atm/MCV/compiler.cfg`中将条件预编译参数**DEF**中`-DCUBE`替换为`-DLONLAT`，安装方法与全球模式相同。

## 运行MCV模式

### 运行前准备

- 初始场数据准备

将MPS生成的初始场数据mcv_input_$YYYYMMDDhhmmss.nc链接或拷贝到目录PMCV/run/atm/MCV/data。

- 物理静态数据准备 

```bash
$ cd PMCV/run/atm/MCV/data 
$ ./link_clim.sh   #确保已设置环境变量FIX_DATA
```

- 模式配置文件准备

需要修改以下配置文件（参考版本提供的自由度为1°的示例）。

 - namelist.atm : 模式运行控制参数，包括分辨率、起报时间、方案选择等。
 - input.nml : 物理参数化方案配置文件。
 - env_run.xml

```bash
# 配置文件在PMCV/run/atm/MCV/data目录下 
# 生成物理过程配置文件input.nml
$ vi namelist.atm   #修改模式分辨率、积分时间、输出频次dumpstep等参数 

$ ./make_input_nml.sh res imp_physics
 #res指模式分辨率，数值代表MCV立方球网格每个面的VIA cells数目，与namelist.atm中nx参数值相同，比如自由度1°的res=45； 
 #指定微物理方案,imp_physics= 11 (默认，GFDL方案)， 99 (zhao方案)
 
$ vi Experiments/PMCV/CCPL_dir/config/all/env_run.xml 
 # 修改起报日期start_date参数
```

### 运行模式

两种方法：

- runcase提交作业

 在Experiments/PMCV目录下提交runcase脚本。
 
 注意只能在PMCV目录下提交作业
 
 ```bash
 $ cd Experiments/PMCV 
 $ ./runcase
 ```
 
 这种提交方式如果需要修改计算核数，必须提前修改配置文件Experiments/PMCV/config/common/case.conf并执行configure脚本使设置生效。
 
- 直接提交作业脚本

 如果Experiments/PMCV/job_logs目录下已存在类似job.submit.xxxx作业脚本，可以在PMCV目录下直接使用sbatch提交该作业脚本，修改作业运行参数不需要执行configure脚本。
 
 ```bash
 $ cd Experiments/PMCV  # 必须在该目录下提交，否则会运行出错
 $ sbatch job_logs/job.submit.xxxx
 ```
 
 模式标准输出和标准错误会重定向到log文件中，job_logs目录下日志文件PMCV.error.xxxx, PMCV.output.xxxx （具体与作业脚本设置有关）。
 





