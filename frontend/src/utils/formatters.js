// Utility functions for formatting data
export const formatPrice = (price) => {
  if (!price) return "N/A"
  return `₹${(price / 100000).toFixed(1)}L`
}

export const formatYear = (year) => {
  return year ? year.toString() : "N/A"
}

export const sortByYear = (data) => {
  return [...data].sort((a, b) => a.year - b.year)
}

export const filterByArea = (data, area) => {
  return data.filter((item) => item.area.toLowerCase() === area.toLowerCase())
}

export const calculateGrowth = (current, previous) => {
  if (!previous || previous === 0) return 0
  return (((current - previous) / previous) * 100).toFixed(2)
}
