export const getCreatedAt = createdAt => {
  if (!createdAt) return []
  const [start, end] = createdAt

  return [start, end]
}
