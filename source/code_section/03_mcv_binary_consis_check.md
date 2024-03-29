# MCV并行正确性检查

在模式开发过程中，经常需要测试和排查研发代码的正确性。其中一种检查技术是变量全场校验和(checksum)。
不同MPI进程规模变量的全场校验和应该相同，如果结果不同，说明程序可能存在问题，需要排查诊断。

C-Coupler提供了注册场的自动校验和功能，MCV利用该功能封装成子程序`diag_all_checksum`对MCV所有注册场
进行校验和功能。

由于全场校验和功能开销巨大，建议只有在并行正确性测试和问题诊断时开启该功能。


## 使用方法

- 设置parallel_functions.F90中参数`debug_with_checksum = .true.`。
- 在相应代码部分添加调用子程序，不断缩小问题范围。

```fortran
call diag_all_checksum(hint)  !hint为字符串变量，可以辅助定位代码位置
```

- PMCV/CCPL_dir/config/all/CCPL_report.xml 参数设置如下

```
report_internal_log="off" #关闭coupler内部log信息，避免干扰
report_external_log="off"
report_progress="on"
report_error="on"
flush_log_file="on"
```

- 不同进程规模运行，并保存以下信息

```bash
$ grep "Check sum of" CCPL_dir/run/CCPL_logs/by_executables/MCV/MCV.CCPL.log.0 > diffx.out

类似信息如下
C-Coupler REPORT LOG in the component model "MCV" corresponding to the executable named "MCV", at the current simulation time of 20190712-00000 (the current step number is 0): Check sum of field "qt_pv_1" in mmdiscretizationh, check3 is 18ac9c63aa52227
```

- 查看不同进程配置上述文件是否有差异，如有差异根据hint进行定位

```bash
$ diff diff1.out diff2.out
```


