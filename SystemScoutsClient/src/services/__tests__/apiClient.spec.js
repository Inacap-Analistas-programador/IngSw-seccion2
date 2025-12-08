/**
 * Unit tests for API client service
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import apiClient from '../apiClient'

// Mock fetch
global.fetch = vi.fn()

// Mock localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
}
global.localStorage = localStorageMock

describe('apiClient', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorageMock.getItem.mockReturnValue('mock-token')
  })

  describe('get', () => {
    it('should make GET request with auth token', async () => {
      const mockData = { id: 1, name: 'Test' }
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockData,
      })

      const result = await apiClient.get('/test-endpoint')

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/test-endpoint'),
        expect.objectContaining({
          method: 'GET',
          headers: expect.objectContaining({
            Authorization: 'Bearer mock-token',
          }),
        }),
      )
      expect(result).toEqual(mockData)
    })

    it('should handle 401 unauthorized', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 401,
      })

      await expect(apiClient.get('/test-endpoint')).rejects.toThrow()
    })
  })

  describe('post', () => {
    it('should make POST request with data', async () => {
      const postData = { name: 'New Item' }
      const mockResponse = { id: 1, ...postData }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      const result = await apiClient.post('/test-endpoint', postData)

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/test-endpoint'),
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(postData),
        }),
      )
      expect(result).toEqual(mockResponse)
    })
  })

  describe('put', () => {
    it('should make PUT request with data', async () => {
      const putData = { id: 1, name: 'Updated Item' }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => putData,
      })

      const result = await apiClient.put('/test-endpoint/1', putData)

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/test-endpoint/1'),
        expect.objectContaining({
          method: 'PUT',
        }),
      )
      expect(result).toEqual(putData)
    })
  })

  describe('delete', () => {
    it('should make DELETE request', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({}),
      })

      await apiClient.delete('/test-endpoint/1')

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/test-endpoint/1'),
        expect.objectContaining({
          method: 'DELETE',
        }),
      )
    })
  })
})
