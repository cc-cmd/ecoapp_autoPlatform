import apiClient from './client';
import type { Device } from '@/types';

/**
 * Get list of all test devices.
 */
export async function getDevices(): Promise<Device[]> {
  const response = await apiClient.get<Device[]>('/devices');
  return response.data;
}

/**
 * Trigger device discovery via ADB / iOS tools.
 */
export async function discoverDevices(): Promise<Device[]> {
  const response = await apiClient.post<Device[]>('/devices/discover');
  return response.data;
}
