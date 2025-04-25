const orderMapping = {
  'true': 'asc',
  'false': 'asc',
}

export const getCreatedAt = createdAt => {
  if (!createdAt) return []
  const [start, end] = createdAt

  return [start, end]
}

export const getSortNumQuery = fieldMappings => {
  const result = []
  const route = useRoute()

  if (Object.keys(route.query).length === 0) {
    return [{ key: 'createdAt', order: 'desc' }]
  }
  for (const field in fieldMappings) {
    const { num, sort } = fieldMappings[field]
    if (num in route.query && sort in route.query) {

      const order = orderMapping[route.query[sort]]

      result.push({ key: field, order, num: Number(route.query[num]) })
    }
  }
  result.sort((a, b) => a.num - b.num)
  
  return result
}

export const getLineChartRandomColor = () => {
  const color = [
    {
      borderColor: 'rgba(54, 162, 235, 1)',
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
    },
    {
      borderColor: 'rgba(255, 99, 132,1)',
      backgroundColor: 'rgba(255, 99, 132, 0.2)',
    },
    {
      borderColor: 'rgba(75, 192, 192, 1)',
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
    },
    {
      borderColor: 'rgba(255, 206, 86, 1)',
      backgroundColor: 'rgba(255, 206, 86, 0.2)',
    },
    {
      borderColor: 'rgba(255, 159, 64, 1)',
      backgroundColor: 'rgba(255, 159, 64, 0.2)',
    },
    {
      borderColor: 'rgba(153, 102, 255, 1)',
      backgroundColor: 'rgba(153, 102, 255, 0.2)',
    },
  ]

  return color[Math.floor(Math.random() * color.length)]
}
