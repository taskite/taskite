import { initials } from '@dicebear/collection'
import { createAvatar } from '@dicebear/core'
import { getPresignUrlAPI, fileUploadAPI } from './api'
import { message } from 'ant-design-vue'

export const generateAvatar = (seedValue, radius = 50) => {
  return createAvatar(initials, {
    seed: seedValue,
    scale: 70,
    backgroundColor: ['B490FF'],
    radius: radius,
  }).toDataUri()
}

export const uploadRequestHandler = async ({ file, onSuccess, onError }) => {
  const loadingMessage = message.loading('Uploading ...', 0)
  try {
    const { data } = await getPresignUrlAPI(file.name, file.type)
    console.log(data)

    await fileUploadAPI(data.fileUploadUrl, file, data.fileKey)

    // Close loading message
    loadingMessage()

    // // Show success message
    message.success('Upload successful')

    // onSuccess()
    return {
      fileKey: data.fileKey,
      fileSrc: data.fileSrc,
    }
  } catch (error) {
    // Close loading message
    loadingMessage()

    // Show error message
    message.error('Upload failed')

    onError(error)
  }
}
