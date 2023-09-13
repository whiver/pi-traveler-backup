#!/bin/bash

unmount_devices() {
    udisksctl unmount -b $inputPartition
    udisksctl unmount -b $outputPartition
}

abort() {
    echo "Received signal, exiting..."

    rsyncPid=$(pgrep rsync)
    
    if [ -n "$rsyncPid" ]
    then
        echo "Rsync still running, waiting..."
        timeout 10 tail --pid=$rsyncPid -f /dev/null
    fi

    echo "Try unmounting partitions..."
    unmount_devices
    exit 1
}

# Intercept interrupts to unmount properly the drives before exit
trap "abort" SIGINT SIGTERM

inputDrive=$(readlink -e $(ls /dev/disk/by-id/usb-* | grep $(cat /sys/bus/usb/devices/1-1.2/serial) | head -n 1))
outputDrive=$(readlink -e $(ls /dev/disk/by-id/usb-* | grep $(cat /sys/bus/usb/devices/1-1.3/serial) | head -n 1))

inputPartition="${inputDrive}1"
outputPartition="${outputDrive}1"

# Unmount drives in case they are already mounted
udisksctl unmount -b $inputPartition && echo "⇒ Unmount already mounted ${inputPartition}."
udisksctl unmount -b $outputPartition && echo "⇒ Unmount already mounted ${outputPartition}."

inputMountPath=$(udisksctl mount -b $inputPartition --no-user-interaction | sed "s|.*\(/media/${USER}\)|\1|")
outputMountPath=$(udisksctl mount -b $outputPartition --no-user-interaction | sed "s|.*\(/media/${USER}\)|\1|")

if ([ -n "$inputMountPath" ] && [ -n "$outputMountPath" ])
then
    echo "⇒ Mounted $inputPartition (${inputMountPath}) and $outputPartition (${outputMountPath})."
else
    echo "Could not mount partitions."
    exit 1
fi

echo "⇒ Will backup $inputMountPath (${inputPartition}) to ${outputMountPath} (${outputPartition})..."

rsync \
    -va --prune-empty-dirs --progress --info=progress2 --info=name0 \
    "$inputMountPath" "$outputMountPath" \
    | python3 /home/$USER/progress.py

unmount_devices
