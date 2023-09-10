export const getCreatedAt = createdAt => {
  if (!createdAt) return []
  const [start, end] = createdAt

  return [start, end]
}

export const getSortNumQuery = fieldMappings => {
  const result = []
  const route = useRoute()

  for (const field in fieldMappings) {
    const { num, sort } = fieldMappings[field]
    if (num in route.query && sort in route.query) {
      const order = route.query[sort] === 'true' ? 'asc' : 'desc'

      result.push({ key: field, order, num: Number(route.query[num]) })
    }
  }
  result.sort((a, b) => a.num - b.num)
  
  return result
}
