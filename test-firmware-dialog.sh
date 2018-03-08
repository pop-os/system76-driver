echo "Showing standard dialog"

export FIRMWARE_DATA=$(cat <<EOF
{
    "desktop": "gnome",
    "notification": false,
    "flash": true,
    "current": {
        "bios": "current_bios",
        "ec": "current_ec",
        "ec2": "current_ec2",
        "me": "current_me"
    },
    "latest": {
        "bios": "latest_bios",
        "ec": "latest_ec",
        "ec2": "latest_ec2",
        "me": "latest_me"
    },
    "changelog": [{
        "bios": "changelog_bios",
        "ec": "changelog_ec",
        "ec2": "changelog_ec2",
        "me": "changelog_me",
        "description": "changelog_description"
    }]
}
EOF
)

./system76-firmware-dialog

echo "Showing error dialog"
FIRMWARE_ERROR="Test error" ./system76-firmware-dialog

echo "Showing network dialog"
FIRMWARE_NETWORK=1 ./system76-firmware-dialog

echo "Showing success dialog"
FIRMWARE_SUCCESS=1 ./system76-firmware-dialog
