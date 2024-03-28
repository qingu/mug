# 常见问题汇总

## MCV模式运行日志提示” Error: datetime from coupler env_run.nml not match namelist”错误。

原因：MCV模式namelist.atm设置的模拟起报时间与env_run.xml不一致。

解决方法：修改Experiments/PMCV/CCPL_dir/config/all/env_run.xml中节点值start_second和start_second与namelist.atm匹配。

