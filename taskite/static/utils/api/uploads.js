import { client } from './client'

export const getPresignUrlAPI = (fileName, fileType) =>
  client.post(`/uploads/presigned-url`, { fileName, fileType })

export const confirmUploadAPI = (url, file, fileName) => {
  return client.put(url, file, {
    headers: {
      'Content-Disposition': `attachment; filename=${fileName}`
    },
  })
}


export const fileUploadAPI = (url, file, fileName) => {
  return client.put(url, file, {
    headers: {
      'Content-Disposition': `attachment; filename=${fileName}`
    },
  })
}