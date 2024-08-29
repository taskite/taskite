import { initials } from "@dicebear/collection"
import { createAvatar } from "@dicebear/core"

export const generateAvatar = (seedValue) => {
    return createAvatar(initials, {
        seed: seedValue,
        scale: 70,
        backgroundColor: ['8e8e8e'],
        radius: 50
    }).toDataUri()
}