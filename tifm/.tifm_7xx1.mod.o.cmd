cmd_/home/carl/workspace/system76-driver/system76-driver-1.9.1/opt/system76/system76-driver/src/tifm/tifm_7xx1.mod.o := gcc -m32 -Wp,-MD,/home/carl/workspace/system76-driver/system76-driver-1.9.1/opt/system76/system76-driver/src/tifm/.tifm_7xx1.mod.o.d  -nostdinc -isystem /usr/lib/gcc/i486-linux-gnu/4.1.2/include -D__KERNEL__ -Iinclude  -include include/linux/autoconf.h -Wall -Wundef -Wstrict-prototypes -Wno-trigraphs -fno-strict-aliasing -fno-common -fno-stack-protector -O2 -fomit-frame-pointer -fasynchronous-unwind-tables -pipe -msoft-float -mpreferred-stack-boundary=2  -march=i586 -mtune=generic -mregparm=3 -ffreestanding -Iinclude/asm-i386/mach-default -Wdeclaration-after-statement -Wno-pointer-sign    -D"KBUILD_STR(s)=\#s" -D"KBUILD_BASENAME=KBUILD_STR(tifm_7xx1)"  -D"KBUILD_MODNAME=KBUILD_STR(tifm_7xx1)" -DMODULE -c -o /home/carl/workspace/system76-driver/system76-driver-1.9.1/opt/system76/system76-driver/src/tifm/tifm_7xx1.mod.o /home/carl/workspace/system76-driver/system76-driver-1.9.1/opt/system76/system76-driver/src/tifm/tifm_7xx1.mod.c

deps_/home/carl/workspace/system76-driver/system76-driver-1.9.1/opt/system76/system76-driver/src/tifm/tifm_7xx1.mod.o := \
  /home/carl/workspace/system76-driver/system76-driver-1.9.1/opt/system76/system76-driver/src/tifm/tifm_7xx1.mod.c \
    $(wildcard include/config/module/unload.h) \
  include/linux/module.h \
    $(wildcard include/config/modules.h) \
    $(wildcard include/config/modversions.h) \
    $(wildcard include/config/kallsyms.h) \
  include/linux/sched.h \
    $(wildcard include/config/detect/softlockup.h) \
    $(wildcard include/config/split/ptlock/cpus.h) \
    $(wildcard include/config/keys.h) \
    $(wildcard include/config/inotify.h) \
    $(wildcard include/config/schedstats.h) \
    $(wildcard include/config/smp.h) \
    $(wildcard include/config/debug/mutexes.h) \
    $(wildcard include/config/bsd/process/acct.h) \
    $(wildcard include/config/numa.h) \
    $(wildcard include/config/cpusets.h) \
    $(wildcard include/config/compat.h) \
    $(wildcard include/config/hotplug/cpu.h) \
    $(wildcard include/config/preempt.h) \
    $(wildcard include/config/pm.h) \
  include/linux/auxvec.h \
  include/asm/auxvec.h \
  include/asm/param.h \
    $(wildcard include/config/hz.h) \
  include/linux/capability.h \
  include/linux/types.h \
    $(wildcard include/config/uid16.h) \
  include/linux/posix_types.h \
  include/linux/stddef.h \
  include/linux/compiler.h \
  include/linux/compiler-gcc4.h \
    $(wildcard include/config/forced/inlining.h) \
  include/linux/compiler-gcc.h \
  include/asm/posix_types.h \
  include/asm/types.h \
    $(wildcard include/config/highmem64g.h) \
    $(wildcard include/config/lbd.h) \
    $(wildcard include/config/lsf.h) \
  include/linux/spinlock.h \
    $(wildcard include/config/debug/spinlock.h) \
  include/linux/preempt.h \
    $(wildcard include/config/debug/preempt.h) \
  include/linux/thread_info.h \
  include/linux/bitops.h \
  include/asm/bitops.h \
  include/asm/alternative.h \
  include/asm-generic/bitops/sched.h \
  include/asm-generic/bitops/hweight.h \
  include/asm-generic/bitops/fls64.h \
  include/asm-generic/bitops/ext2-non-atomic.h \
  include/asm-generic/bitops/le.h \
  include/asm/byteorder.h \
    $(wildcard include/config/x86/bswap.h) \
  include/linux/byteorder/little_endian.h \
  include/linux/byteorder/swab.h \
  include/linux/byteorder/generic.h \
  include/asm-generic/bitops/minix.h \
  include/asm/thread_info.h \
    $(wildcard include/config/4kstacks.h) \
    $(wildcard include/config/debug/stack/usage.h) \
  include/asm/page.h \
    $(wildcard include/config/x86/use/3dnow.h) \
    $(wildcard include/config/x86/pae.h) \
    $(wildcard include/config/hugetlb/page.h) \
    $(wildcard include/config/highmem4g.h) \
    $(wildcard include/config/page/offset.h) \
    $(wildcard include/config/physical/start.h) \
    $(wildcard include/config/flatmem.h) \
  include/asm/page_offset.h \
    $(wildcard include/config/05gb.h) \
    $(wildcard include/config/1gb.h) \
    $(wildcard include/config/2gb.h) \
    $(wildcard include/config/3gb.h) \
  include/asm-generic/memory_model.h \
    $(wildcard include/config/discontigmem.h) \
    $(wildcard include/config/out/of/line/pfn/to/page.h) \
    $(wildcard include/config/sparsemem.h) \
  include/asm-generic/page.h \
  include/asm/processor.h \
    $(wildcard include/config/x86/ht.h) \
    $(wildcard include/config/mk8.h) \
    $(wildcard include/config/mk7.h) \
    $(wildcard include/config/mtrr.h) \
    $(wildcard include/config/x86/mce.h) \
  include/asm/vm86.h \
    $(wildcard include/config/vm86.h) \
  include/asm/math_emu.h \
  include/asm/sigcontext.h \
  include/asm/segment.h \
  include/asm/cpufeature.h \
  include/asm/msr.h \
  include/asm/system.h \
    $(wildcard include/config/x86/cmpxchg64.h) \
    $(wildcard include/config/x86/cmpxchg.h) \
    $(wildcard include/config/x86/oostore.h) \
  include/linux/kernel.h \
    $(wildcard include/config/preempt/voluntary.h) \
    $(wildcard include/config/debug/spinlock/sleep.h) \
    $(wildcard include/config/printk.h) \
  /usr/lib/gcc/i486-linux-gnu/4.1.2/include/stdarg.h \
  include/linux/linkage.h \
  include/asm/linkage.h \
    $(wildcard include/config/x86/alignment/16.h) \
  include/asm/bug.h \
    $(wildcard include/config/bug.h) \
    $(wildcard include/config/debug/bugverbose.h) \
  include/asm-generic/bug.h \
  include/linux/cache.h \
  include/asm/cache.h \
    $(wildcard include/config/x86/l1/cache/shift.h) \
  include/linux/threads.h \
    $(wildcard include/config/nr/cpus.h) \
    $(wildcard include/config/base/small.h) \
  include/asm/percpu.h \
  include/asm-generic/percpu.h \
  include/linux/cpumask.h \
  include/linux/bitmap.h \
  include/linux/string.h \
  include/asm/string.h \
  include/linux/stringify.h \
  include/linux/spinlock_types.h \
  include/asm/spinlock_types.h \
  include/asm/spinlock.h \
    $(wildcard include/config/x86/ppro/fence.h) \
  include/asm/atomic.h \
    $(wildcard include/config/m386.h) \
  include/asm-generic/atomic.h \
  include/asm/rwlock.h \
  include/linux/spinlock_api_smp.h \
  include/asm/current.h \
  include/linux/timex.h \
    $(wildcard include/config/time/interpolation.h) \
  include/linux/time.h \
  include/linux/seqlock.h \
  include/asm/timex.h \
    $(wildcard include/config/x86/elan.h) \
    $(wildcard include/config/x86/tsc.h) \
    $(wildcard include/config/x86/generic.h) \
  include/linux/jiffies.h \
  include/linux/calc64.h \
  include/asm/div64.h \
  include/linux/rbtree.h \
  include/linux/errno.h \
  include/asm/errno.h \
  include/asm-generic/errno.h \
  include/asm-generic/errno-base.h \
  include/linux/nodemask.h \
  include/linux/numa.h \
    $(wildcard include/config/nodes/shift.h) \
  include/asm/semaphore.h \
  include/linux/wait.h \
  include/linux/list.h \
  include/linux/prefetch.h \
  include/linux/rwsem.h \
    $(wildcard include/config/rwsem/generic/spinlock.h) \
  include/asm/rwsem.h \
  include/asm/ptrace.h \
    $(wildcard include/config/frame/pointer.h) \
  include/asm/mmu.h \
  include/asm/cputime.h \
  include/asm-generic/cputime.h \
  include/linux/smp.h \
  include/asm/smp.h \
    $(wildcard include/config/x86/local/apic.h) \
    $(wildcard include/config/x86/io/apic.h) \
  include/asm/fixmap.h \
    $(wildcard include/config/highmem.h) \
    $(wildcard include/config/x86/visws/apic.h) \
    $(wildcard include/config/x86/f00f/bug.h) \
    $(wildcard include/config/x86/cyclone/timer.h) \
    $(wildcard include/config/acpi.h) \
    $(wildcard include/config/pci/mmconfig.h) \
  include/asm/acpi.h \
    $(wildcard include/config/acpi/sleep.h) \
  include/acpi/pdc_intel.h \
  include/asm/apicdef.h \
  include/asm/kmap_types.h \
    $(wildcard include/config/debug/highmem.h) \
  include/asm/mpspec.h \
  include/asm/mpspec_def.h \
  include/asm-i386/mach-default/mach_mpspec.h \
  include/asm/io_apic.h \
    $(wildcard include/config/pci/msi.h) \
  include/asm/apic.h \
    $(wildcard include/config/x86/good/apic.h) \
    $(wildcard include/config/x86/up/apic/default/off.h) \
  include/linux/pm.h \
  include/asm-i386/mach-default/mach_apicdef.h \
  include/linux/sem.h \
    $(wildcard include/config/sysvipc.h) \
  include/linux/ipc.h \
  include/asm/ipcbuf.h \
  include/asm/sembuf.h \
  include/linux/signal.h \
  include/asm/signal.h \
  include/asm-generic/signal.h \
  include/asm/siginfo.h \
  include/asm-generic/siginfo.h \
  include/linux/securebits.h \
  include/linux/fs_struct.h \
  include/linux/completion.h \
  include/linux/pid.h \
  include/linux/rcupdate.h \
  include/linux/percpu.h \
  include/linux/slab.h \
    $(wildcard include/config/slob.h) \
    $(wildcard include/config/debug/slab.h) \
  include/linux/gfp.h \
    $(wildcard include/config/dma/is/dma32.h) \
  include/linux/mmzone.h \
    $(wildcard include/config/force/max/zoneorder.h) \
    $(wildcard include/config/memory/hotplug.h) \
    $(wildcard include/config/flat/node/mem/map.h) \
    $(wildcard include/config/have/memory/present.h) \
    $(wildcard include/config/need/node/memmap/size.h) \
    $(wildcard include/config/need/multiple/nodes.h) \
    $(wildcard include/config/have/arch/early/pfn/to/nid.h) \
    $(wildcard include/config/sparsemem/extreme.h) \
  include/linux/init.h \
    $(wildcard include/config/hotplug.h) \
    $(wildcard include/config/acpi/hotplug/memory.h) \
    $(wildcard include/config/acpi/hotplug/memory/module.h) \
  include/linux/memory_hotplug.h \
  include/linux/notifier.h \
  include/linux/mutex.h \
  include/linux/topology.h \
    $(wildcard include/config/sched/smt.h) \
    $(wildcard include/config/sched/mc.h) \
  include/asm/topology.h \
  include/asm-generic/topology.h \
  include/linux/kmalloc_sizes.h \
    $(wildcard include/config/mmu.h) \
    $(wildcard include/config/large/allocs.h) \
  include/linux/seccomp.h \
    $(wildcard include/config/seccomp.h) \
  include/asm/seccomp.h \
  include/linux/unistd.h \
  include/asm/unistd.h \
  include/linux/futex.h \
    $(wildcard include/config/futex.h) \
  include/linux/param.h \
  include/linux/resource.h \
  include/asm/resource.h \
  include/asm-generic/resource.h \
  include/linux/timer.h \
  include/linux/hrtimer.h \
    $(wildcard include/config/no/idle/hz.h) \
  include/linux/ktime.h \
    $(wildcard include/config/ktime/scalar.h) \
  include/linux/aio.h \
  include/linux/workqueue.h \
  include/linux/aio_abi.h \
  include/linux/stat.h \
  include/asm/stat.h \
  include/linux/kmod.h \
    $(wildcard include/config/kmod.h) \
  include/linux/elf.h \
  include/linux/elf-em.h \
  include/asm/elf.h \
  include/asm/user.h \
  include/linux/utsname.h \
  include/linux/kobject.h \
  include/linux/sysfs.h \
    $(wildcard include/config/sysfs.h) \
  include/linux/kref.h \
  include/linux/moduleparam.h \
  include/asm/local.h \
  include/asm/module.h \
    $(wildcard include/config/m486.h) \
    $(wildcard include/config/m586.h) \
    $(wildcard include/config/m586tsc.h) \
    $(wildcard include/config/m586mmx.h) \
    $(wildcard include/config/m686.h) \
    $(wildcard include/config/mpentiumii.h) \
    $(wildcard include/config/mpentiumiii.h) \
    $(wildcard include/config/mpentiumm.h) \
    $(wildcard include/config/mpentium4.h) \
    $(wildcard include/config/mk6.h) \
    $(wildcard include/config/mcrusoe.h) \
    $(wildcard include/config/mefficeon.h) \
    $(wildcard include/config/mwinchipc6.h) \
    $(wildcard include/config/mwinchip2.h) \
    $(wildcard include/config/mwinchip3d.h) \
    $(wildcard include/config/mcyrixiii.h) \
    $(wildcard include/config/mviac3/2.h) \
    $(wildcard include/config/mgeodegx1.h) \
    $(wildcard include/config/mgeode/lx.h) \
    $(wildcard include/config/regparm.h) \
  include/linux/vermagic.h \
  include/linux/version.h \

/home/carl/workspace/system76-driver/system76-driver-1.9.1/opt/system76/system76-driver/src/tifm/tifm_7xx1.mod.o: $(deps_/home/carl/workspace/system76-driver/system76-driver-1.9.1/opt/system76/system76-driver/src/tifm/tifm_7xx1.mod.o)

$(deps_/home/carl/workspace/system76-driver/system76-driver-1.9.1/opt/system76/system76-driver/src/tifm/tifm_7xx1.mod.o):
