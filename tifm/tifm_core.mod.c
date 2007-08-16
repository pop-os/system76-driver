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
	{ 0x50b23059, "bus_register" },
	{ 0x1e824840, "class_register" },
	{ 0x9f793fc6, "driver_register" },
	{ 0x55e2babe, "mem_map" },
	{ 0xb549429b, "malloc_sizes" },
	{ 0x1bcd461f, "_spin_lock" },
	{ 0x589df9e6, "__create_workqueue" },
	{ 0x648f6c9d, "class_device_put" },
	{ 0xf0e66c10, "class_device_del" },
	{ 0x1b7d4074, "printk" },
	{ 0x957d8741, "class_unregister" },
	{ 0x688832ae, "driver_unregister" },
	{ 0x4ab9e566, "destroy_workqueue" },
	{ 0x63b8943f, "bus_unregister" },
	{ 0xa7409aaf, "idr_remove" },
	{ 0x52a7207f, "idr_pre_get" },
	{ 0xbb4eab24, "class_device_add" },
	{ 0xbe4bc9a8, "put_device" },
	{ 0x6b2dc060, "dump_stack" },
	{ 0xef8cbdd3, "get_device" },
	{ 0xa27b885f, "kmem_cache_zalloc" },
	{ 0x37a0cba, "kfree" },
	{ 0x25da070, "snprintf" },
	{ 0x2d29e50a, "idr_get_new" },
	{ 0x2ab6ebbe, "class_device_initialize" },
	{ 0x45e87ae6, "add_uevent_var" },
};

static const char __module_depends[]
__attribute_used__
__attribute__((section(".modinfo"))) =
"depends=";


MODULE_INFO(srcversion, "2B4C32836A3EEFF6FCE6F36");
