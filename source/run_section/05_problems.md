# 常见问题汇总

## MCV模式运行日志提示” Error: datetime from coupler env_run.nml not match namelist”错误。

原因：MCV模式namelist.atm设置的模拟起报时间与env_run.xml不一致。

解决方法：修改Experiments/PMCV/CCPL_dir/config/all/env_run.xml中节点值start_date和start_second组合与namelist.atm匹配。其中start_second代表一天中经过的秒数。

## MCV模式运行日志提示C-Coupler初始化失败错误。

原因：如果PMCV.out.xxx文件中提示如下错误

```
C-Coupler REPORT ERROR: Fail to initialize C-Coupler: the directory ("/.../PMCV/job_logs/CCPL_dir/config") for configuration files of C-Coupler does not exit.
```

表明作业提交脚本没有在PMCV目录下提交。C-Coupler需要设置PMCV为工作目录，读取的配置文件目录是工作目录的相对位置。

解决方法：在PMCV目录下提交作业脚本或者在作业提交脚本中设置当前工作目录为PMCV目录。



