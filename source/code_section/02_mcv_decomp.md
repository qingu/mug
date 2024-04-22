# MCV并行剖分方案

MCV模式采用MPI与OpenMP混合并行方案。在MPI进程并行层级采用水平空间并行剖分方式，对于MCV全球模式由于计算网格
特点，对运行时进程数有一定限制。MCV全球模式采用立方球网格，其有6个面，目前并行剖分方案不允许一个进程跨越两个面。

因此，MCV全球模式运行时进程数需满足以下两个条件：

- 首先进程数能被6整除;
- 其次进程数能被2/3/5因式分解。

MCV模式动力框架允许1个进程（即串行方式）运行，但物理过程暂不支持串行运行。

你可以使用以下Fortran程序测试哪些进程配置允许被使用。

```fortran
module decomp_info
  implicit none
contains
  logical function allowed_process_num(ntasks,cores_of_one_node)
    implicit none
    integer,parameter  :: ntiles = 6
    integer,intent(in) :: ntasks
    ! cores_of_one_node: require all cores of the node to be utilized
    integer,optional,intent(in) :: cores_of_one_node
    integer :: factors(3),iter,i
    logical :: changed

    factors(1:3)=[2,3,5]

    if(ntasks == 1) then
      allowed_process_num = .true.
      return
    endif

    if(mod(ntasks,ntiles) /= 0) then
      allowed_process_num  = .false.
      return
    endif

    if(present(cores_of_one_node)) then
      if(mod(ntasks,cores_of_one_node) /= 0) then
        allowed_process_num  = .false.
        return
      endif
    endif

    changed = .true.
    iter = ntasks
    do while(changed)
      changed = .false.
      do i=1,3
        if(mod(iter,factors(i)) == 0) then
          changed = .true.
          iter = iter / factors(i)
        endif
      enddo
    enddo
    if(iter == 1) then
      allowed_process_num = .true.
    else
      allowed_process_num = .false.
    endif
    return
  end function allowed_process_num
end module decomp_info

program main
  use decomp_info
  implicit none

  integer :: i,cores_node
  logical :: allowed

  cores_node = 64  ! one node has 64 cores
  do i=1,100000
    allowed = allowed_process_num(i,cores_node)
    if(allowed) print*, "num of tasks = ",i," allowed"
  enddo
end
```

其中函数`allowed_process_num`第二个（可选）参数表示计算节点核心数，如果传递该参数，
表明需用满节点核心数。
