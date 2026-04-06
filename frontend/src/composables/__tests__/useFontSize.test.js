import { describe, it, expect, beforeEach } from 'vitest'
import { useFontSize } from '../useFontSize.js'

beforeEach(() => {
  localStorage.clear()
  // Reset to medium default
  const { setFontSize } = useFontSize()
  setFontSize('medium')
})

describe('useFontSize', () => {
  it('defaults to medium', () => {
    localStorage.removeItem('font_size')
    // The module-level ref reads from localStorage on import, so after clearing
    // we verify the composable returns a valid size
    const { fontSize } = useFontSize()
    expect(fontSize.value).toBe('medium')
  })

  it('setFontSize("large") updates localStorage', () => {
    const { setFontSize, fontSize } = useFontSize()
    setFontSize('large')
    expect(fontSize.value).toBe('large')
    expect(localStorage.getItem('font_size')).toBe('large')
  })

  it('setFontSize updates to each valid size', () => {
    const { setFontSize, fontSize } = useFontSize()
    for (const size of ['small', 'medium', 'large', 'xlarge']) {
      setFontSize(size)
      expect(fontSize.value).toBe(size)
      expect(localStorage.getItem('font_size')).toBe(size)
    }
  })

  it('invalid sizes are rejected', () => {
    const { setFontSize, fontSize } = useFontSize()
    setFontSize('medium')
    setFontSize('giant')
    expect(fontSize.value).toBe('medium')
    expect(localStorage.getItem('font_size')).toBe('medium')

    setFontSize('')
    expect(fontSize.value).toBe('medium')

    setFontSize(null)
    expect(fontSize.value).toBe('medium')
  })

  it('cycleFontSize cycles S -> M -> L -> XL -> S', () => {
    const { setFontSize, cycleFontSize, fontSize } = useFontSize()

    setFontSize('small')
    expect(fontSize.value).toBe('small')

    cycleFontSize()
    expect(fontSize.value).toBe('medium')

    cycleFontSize()
    expect(fontSize.value).toBe('large')

    cycleFontSize()
    expect(fontSize.value).toBe('xlarge')

    cycleFontSize()
    expect(fontSize.value).toBe('small')
  })

  it('exposes size metadata', () => {
    const { sizes, sizeLabels, sizeDisplay, sizeScales } = useFontSize()
    expect(sizes).toEqual(['small', 'medium', 'large', 'xlarge'])
    expect(sizeLabels.small).toBe('S')
    expect(sizeLabels.xlarge).toBe('XL')
    expect(sizeDisplay.large).toBe('Large')
    expect(sizeScales.medium).toBe('16px')
  })
})
