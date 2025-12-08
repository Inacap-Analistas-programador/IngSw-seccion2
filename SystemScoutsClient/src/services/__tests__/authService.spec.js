/**
 * Unit tests for authentication service
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import authService from '../authService'

// Mock localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
}
global.localStorage = localStorageMock

// Mock fetch
global.fetch = vi.fn()

describe('authService', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorageMock.getItem.mockReturnValue(null)
  })

  describe('login', () => {
    it('should store token on successful login', async () => {
      const mockResponse = {
        access: 'mock-access-token',
        refresh: 'mock-refresh-token',
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      const result = await authService.login('testuser', 'testpass')

      expect(result).toEqual(mockResponse)
      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        'access_token',
        'mock-access-token',
      )
      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        'refresh_token',
        'mock-refresh-token',
      )
    })

    it('should throw error on failed login', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 401,
      })

      await expect(authService.login('testuser', 'wrongpass')).rejects.toThrow()
    })
  })

  describe('logout', () => {
    it('should clear tokens from localStorage', () => {
      authService.logout()

      expect(localStorageMock.removeItem).toHaveBeenCalledWith('access_token')
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('refresh_token')
    })
  })

  describe('getToken', () => {
    it('should return token from localStorage', () => {
      localStorageMock.getItem.mockReturnValue('mock-token')

      const token = authService.getToken()

      expect(token).toBe('mock-token')
      expect(localStorageMock.getItem).toHaveBeenCalledWith('access_token')
    })

    it('should return null if no token exists', () => {
      localStorageMock.getItem.mockReturnValue(null)

      const token = authService.getToken()

      expect(token).toBeNull()
    })
  })

  describe('isAuthenticated', () => {
    it('should return true if token exists', () => {
      localStorageMock.getItem.mockReturnValue('mock-token')

      expect(authService.isAuthenticated()).toBe(true)
    })

    it('should return false if no token exists', () => {
      localStorageMock.getItem.mockReturnValue(null)

      expect(authService.isAuthenticated()).toBe(false)
    })
  })
})
