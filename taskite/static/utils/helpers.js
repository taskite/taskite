import { initials } from "@dicebear/collection"
import { createAvatar } from "@dicebear/core"

export const generateAvatar = (seedValue, radius = 50) => {
    return createAvatar(initials, {
        seed: seedValue,
        scale: 70,
        backgroundColor: ['B490FF'],
        radius: radius
    }).toDataUri()
}