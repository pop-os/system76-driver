#include <linux/module.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

MODULE_INFO(vermagic, VERMAGIC_STRING);

struct module __this_module
__attribute__((section(".gnu.linkonce.this_module"))) = {
 .name = KBUILD_MODNAME,
 .init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
 .exit = cleanup_module,
#endif
};

static const struct modversion_info ____versions[]
__attribute_used__
__attribute__((section("__versions"))) = {
	{ 0xaa439674, "struct_module" },
	{ 0x5611e4ec, "param_get_bool" },
	{ 0xdc76cbcb, "param_set_bool" },
	{ 0xefa7dfba, "mmc_remove_host" },
	{ 0x865edc9b, "finish_wait" },
	{ 0x17d59d01, "schedule_timeout" },
	{ 0xc8f02aeb, "prepare_to_wait" },
	{ 0xc8b57c27, "autoremove_wake_function" },
	{ 0xbe298427, "tifm_map_sg" },
	{ 0x76d25c99, "mmc_free_host" },
	{ 0xf9a482f9, "msleep" },
	{ 0xd0b91f9b, "init_timer" },
	{ 0xac6d9a92, "mmc_alloc_host" },
	{ 0x59968f3c, "__wake_up" },
	{ 0xc006b69, "kmap" },
	{ 0x7bf40ef5, "queue_work" },
	{ 0x513a3625, "queue_delayed_work" },
	{ 0xc659d5a, "del_timer_sync" },
	{ 0x1bcd461f, "_spin_lock" },
	{ 0xe7967210, "mmc_add_host" },
	{ 0xf91208c0, "kunmap" },
	{ 0x7972ebf5, "mmc_request_done" },
	{ 0xa20fdde, "_spin_unlock_irqrestore" },
	{ 0x38b2fda0, "tifm_unmap_sg" },
	{ 0x87cddf59, "_spin_lock_irqsave" },
	{ 0x873baf19, "tifm_register_driver" },
	{ 0xbe020513, "tifm_eject" },
	{ 0x1b7d4074, "printk" },
	{ 0xd0e5c943, "tifm_unregister_driver" },
};

static const char __module_depends[]
__attribute_used__
__attribute__((section(".modinfo"))) =
"depends=mmc_core,tifm_core";


MODULE_INFO(srcversion, "015A177041B0D2D65735C8B");
