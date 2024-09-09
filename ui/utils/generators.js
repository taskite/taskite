import { initials } from "@dicebear/collection"
import { createAvatar } from "@dicebear/core"

export const generateAvatar = (seedValue) => {
    return createAvatar(initials, {
        seed: seedValue,
        scale: 70,
        backgroundColor: ['8a7c9e'],
        radius: 50
    }).toDataUri()
}