import type { InventoryItem, UserProfile } from "types/contracts";

import { mockInventory, mockProfile } from "./catalog";

interface MockState {
  profile: UserProfile;
  inventory: InventoryItem[];
}

const STORE_KEY = "meituan-cloud-fridge.mock-state";

function cloneState(state: MockState): MockState {
  return JSON.parse(JSON.stringify(state)) as MockState;
}

export function loadMockState(): MockState {
  const existing = localStorage.getItem(STORE_KEY);
  if (existing) {
    return JSON.parse(existing) as MockState;
  }
  const initialState = cloneState({
    profile: mockProfile,
    inventory: mockInventory,
  });
  saveMockState(initialState);
  return initialState;
}

export function saveMockState(state: MockState) {
  localStorage.setItem(STORE_KEY, JSON.stringify(state));
}

export function resetMockState() {
  localStorage.removeItem(STORE_KEY);
}
