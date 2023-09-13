#!/bin/bash
inputDrive=$(readlink -e $(ls /dev/disk/by-id/usb-* | grep $(cat /sys/bus/usb/devices/1-1.2/serial) | head -n 1))
outputDrive=$(readlink -e $(ls /dev/disk/by-id/usb-* | grep $(cat /sys/bus/usb/devices/1-1.3/serial) | head -n 1))

inputPartition="${inputDrive}1"
outputPartition="${outputDrive}1"

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

udisksctl unmount -b $inputPartition && echo "⇒ Unmount ${inputPartition}."
udisksctl unmount -b $outputPartition && echo "⇒ Unmount ${outputPartition}."
# udisksctl power-off -b $inputPartition && echo "⇒ Power off ${inputPartition}."

#     --include="*/" --include="*.JPG" --include="*.NEF" --exclude="*" \