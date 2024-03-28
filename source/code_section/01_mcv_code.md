# MCV源代码布局

```
models
├── c_coupler
│   ├── build
│   └── src
│       ├── CoR
│       ├── Data_MGT
│       ├── Driver
│       ├── Parallel_MGT
│       ├── PatCC
│       ├── Runtime_MGT
│       ├── Utils
│       └── XML
└── MCV
    └── Sources
        ├── ccpl_dp_coupling
        ├── dynamics
        ├── gfsphysics
        ├── IO
        ├── main.F90
        ├── parallel
        └── share
```

源代码部分包含依赖库c_coupler及MCV模式代码。

其中MCV源代码目录主要功能如下：

- main.F90: MCV模式主程序，控制模式流程
- share: 模式全局数据定义和后处理实现目录
- dynamics: MCV动力框架目录
- gfsphysics: 物理参数化方案目录
- ccpl_dp_coupling: MCV动力物理耦合实现目录，包括物理过程调用驱动
- IO: 模式初始场读入实现目录
- parallel: MCV模式并行软件框架目录



