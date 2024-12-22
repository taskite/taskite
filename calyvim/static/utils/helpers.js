import { initials } from '@dicebear/collection'
import { createAvatar } from '@dicebear/core'
import { getPresignUrlAPI, fileUploadAPI } from './api'
import { message, notification } from 'ant-design-vue'

export const generateAvatar = (seedValue, radius = 50) => {
  return createAvatar(initials, {
    seed: seedValue,
    scale: 70,
    backgroundColor: ['B490FF'],
    radius: radius,
  }).toDataUri()
}

// Helper function to convert file to data URI
const getFileDataURI = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result)
    reader.onerror = reject
    reader.readAsDataURL(file) // This converts the file to a data URI
  })
}

export const uploadRequestHandler = async (
  { file, onSuccess, onError },
  modelName = 'default',
  modelField = 'default'
) => {
  const loadingMessage = message.loading('Uploading ...', 0)
  try {
    const { data } = await getPresignUrlAPI(
      file.name,
      file.type,
      modelName,
      modelField
    )

    // Convert file to data URI
    const dataURI = await getFileDataURI(file)
    await fileUploadAPI(data.fileUploadUrl, file, data.fileKey)

    // Close loading message
    loadingMessage()

    // // Show success message
    message.success('Upload successful')

    onSuccess()
    return {
      fileKey: data.fileKey,
      fileSrc: dataURI,
    }
  } catch (error) {
    // Close loading message
    loadingMessage()

    // Show error message
    message.error('Upload failed')

    onError(error)
  }
}

export const handleResponseError = (error) => {
  console.error('An error occurred:', error)

  let errorMessage = 'An unexpected error occurred. Please try again.'

  if (error.response) {
    const { status, data } = error.response

    if (status === 500) {
      errorMessage = 'A server error occurred. Please try again later or contact support at hey@calyvim.com.'
    } else if (status === 429) {
      errorMessage = 'Too many requests. Please try again later.'
    } else if (data) {
      if (data?.detail) {
        errorMessage = data.detail
      } else if (typeof data === 'string') {
        errorMessage = data
      }
    }
  }

  message.error(errorMessage)
  return errorMessage
}

export const slugify = (text) => {
  return text
    .toString()
    .toLowerCase()
    .replace(/\s+/g, '-') // Replace spaces with -
    .replace(/[^\w\-]+/g, '') // Remove all non-word characters
    .replace(/\-\-+/g, '-') // Replace multiple - with single -
    .replace(/^-+/, '') // Trim - from start of text
    .replace(/-+$/, '') // Trim - from end of text
}

export const processImage = (
  file,
  maxWidth = 200,
  maxHeight = 200,
  maxSizeMB = 2
) => {
  return new Promise((resolve, reject) => {
    // Check file type
    const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png'
    if (!isJpgOrPng) {
      reject(new Error('You can only upload JPG/PNG file!'))
      return
    }

    // Check file size
    const isLt2M = file.size / 1024 / 1024 < maxSizeMB
    if (!isLt2M) {
      reject(new Error(`Image must be smaller than ${maxSizeMB}MB!`))
      return
    }

    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = (e) => {
      const img = new Image()
      img.src = e.target.result
      img.onload = () => {
        const canvas = document.createElement('canvas')
        const ctx = canvas.getContext('2d')

        // Calculate dimensions while maintaining aspect ratio
        let width = img.width
        let height = img.height
        if (width > height) {
          if (width > maxWidth) {
            height = Math.round((height * maxWidth) / width)
            width = maxWidth
          }
        } else {
          if (height > maxHeight) {
            width = Math.round((width * maxHeight) / height)
            height = maxHeight
          }
        }

        canvas.width = width
        canvas.height = height

        ctx.drawImage(img, 0, 0, width, height)

        canvas.toBlob((blob) => {
          const resizedFile = new File([blob], file.name, { type: file.type })
          resolve(resizedFile)
        }, file.type)
      }
    }
  })
}

export const notify = (
  notificationMessage,
  notificationDescription,
  type = 'success',
  duration = 2.5
) => {
  notification.open({
    message: notificationMessage,
    description: notificationDescription,
    placement: 'bottomRight',
    duration: duration,
    style: {
      width: '350px',
      padding: '16px',
      borderLeft: `12px solid ${type === 'success' ? '#8B5CF6' : '#CBD5E1'}`,
    },
  })
}
