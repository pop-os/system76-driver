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
	{ 0x148d8805, "device_register" },
	{ 0x68b452b6, "tifm_free_device" },
	{ 0x25da070, "snprintf" },
	{ 0xd2991bda, "tifm_alloc_device" },
	{ 0xf9a482f9, "msleep" },
	{ 0x7d733561, "tifm_add_adapter" },
	{ 0x26e96637, "request_irq" },
	{ 0x9eac042a, "__ioremap" },
	{ 0xd0b91f9b, "init_timer" },
	{ 0x12f237eb, "__kzalloc" },
	{ 0x9b6aa66f, "tifm_alloc_adapter" },
	{ 0xafd92d9c, "pci_request_regions" },
	{ 0xd066a61e, "pci_set_dma_mask" },
	{ 0x79e8d871, "pci_set_master" },
	{ 0x883fd8bc, "pci_enable_device" },
	{ 0x423163dd, "pci_restore_state" },
	{ 0x72031fc1, "pci_save_state" },
	{ 0x4d9de486, "pci_set_power_state" },
	{ 0x2cbd08f3, "tifm_free_adapter" },
	{ 0x7c97044c, "pci_disable_device" },
	{ 0x4068bed7, "pci_release_regions" },
	{ 0xca8edc37, "pci_intx" },
	{ 0xedc03953, "iounmap" },
	{ 0xab9d1bc1, "tifm_remove_adapter" },
	{ 0xf20dabd8, "free_irq" },
	{ 0x6b04bddf, "flush_workqueue" },
	{ 0x1bcd461f, "_spin_lock" },
	{ 0x50884aff, "__pci_register_driver" },
	{ 0x7bf40ef5, "queue_work" },
	{ 0x648f6c9d, "class_device_put" },
	{ 0xa6269e84, "device_unregister" },
	{ 0xa20fdde, "_spin_unlock_irqrestore" },
	{ 0x1b7d4074, "printk" },
	{ 0x87cddf59, "_spin_lock_irqsave" },
	{ 0x31ef09fc, "class_device_get" },
	{ 0x2020aa65, "pci_unregister_driver" },
};

static const char __module_depends[]
__attribute_used__
__attribute__((section(".modinfo"))) =
"depends=tifm_core";

MODULE_ALIAS("pci:v0000104Cd00008033sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v0000104Cd0000803Bsv*sd*bc*sc*i*");

MODULE_INFO(srcversion, "41235867416F455F32FE7B8");
