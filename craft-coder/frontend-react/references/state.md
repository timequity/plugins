# React State Management

## When to Use What

| Need | Solution |
|------|----------|
| Local UI state | `useState` |
| Derived state | Compute inline or `useMemo` |
| Server data | TanStack Query |
| Global UI state | Zustand |
| Form state | `useState` or React Hook Form |
| URL state | React Router `useSearchParams` |

## useState Patterns

### Object State

```tsx
interface FormState {
  email: string;
  name: string;
}

const [form, setForm] = useState<FormState>({ email: '', name: '' });

// Update single field
setForm(prev => ({ ...prev, email: 'new@example.com' }));

// Update multiple fields
setForm(prev => ({ ...prev, ...updates }));
```

### Array State

```tsx
const [items, setItems] = useState<Item[]>([]);

// Add item
setItems(prev => [...prev, newItem]);

// Remove item
setItems(prev => prev.filter(item => item.id !== id));

// Update item
setItems(prev => prev.map(item =>
  item.id === id ? { ...item, ...updates } : item
));
```

## Zustand Patterns

### Basic Store

```tsx
import { create } from 'zustand';

interface CounterStore {
  count: number;
  increment: () => void;
  decrement: () => void;
  reset: () => void;
}

const useCounterStore = create<CounterStore>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}));

// Usage
const count = useCounterStore((state) => state.count);
const increment = useCounterStore((state) => state.increment);
```

### With Persistence

```tsx
import { persist } from 'zustand/middleware';

const useSettingsStore = create<SettingsStore>()(
  persist(
    (set) => ({
      theme: 'light',
      setTheme: (theme) => set({ theme }),
    }),
    {
      name: 'settings-storage',
    }
  )
);
```

### Slices Pattern

```tsx
// stores/index.ts
import { create } from 'zustand';
import { createAuthSlice, AuthSlice } from './authSlice';
import { createUiSlice, UiSlice } from './uiSlice';

type Store = AuthSlice & UiSlice;

export const useStore = create<Store>()((...a) => ({
  ...createAuthSlice(...a),
  ...createUiSlice(...a),
}));

// stores/authSlice.ts
export interface AuthSlice {
  user: User | null;
  login: (user: User) => void;
  logout: () => void;
}

export const createAuthSlice = (set: SetState<AuthSlice>): AuthSlice => ({
  user: null,
  login: (user) => set({ user }),
  logout: () => set({ user: null }),
});
```

### Async Actions

```tsx
const useStore = create<Store>((set, get) => ({
  users: [],
  loading: false,
  error: null,

  fetchUsers: async () => {
    set({ loading: true, error: null });
    try {
      const users = await api.getUsers();
      set({ users, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },

  addUser: async (data) => {
    const user = await api.createUser(data);
    set((state) => ({ users: [...state.users, user] }));
  },
}));
```

## Context (When Needed)

```tsx
import { createContext, useContext, useState } from 'react';

interface ThemeContextValue {
  theme: 'light' | 'dark';
  toggle: () => void;
}

const ThemeContext = createContext<ThemeContextValue | null>(null);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  const toggle = () => setTheme(t => t === 'light' ? 'dark' : 'light');

  return (
    <ThemeContext.Provider value={{ theme, toggle }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useTheme must be used within ThemeProvider');
  return context;
}
```

## URL State

```tsx
import { useSearchParams } from 'react-router-dom';

function ProductList() {
  const [searchParams, setSearchParams] = useSearchParams();

  const page = Number(searchParams.get('page')) || 1;
  const sort = searchParams.get('sort') || 'newest';

  const setPage = (p: number) => {
    setSearchParams(prev => {
      prev.set('page', String(p));
      return prev;
    });
  };

  const setSort = (s: string) => {
    setSearchParams(prev => {
      prev.set('sort', s);
      prev.delete('page'); // Reset page on sort change
      return prev;
    });
  };

  // ...
}
```

## Performance Tips

```tsx
// 1. Select only what you need from Zustand
const count = useStore(state => state.count); // Good
const store = useStore(); // Bad - re-renders on any change

// 2. Shallow comparison for objects
import { shallow } from 'zustand/shallow';
const { count, increment } = useStore(
  state => ({ count: state.count, increment: state.increment }),
  shallow
);

// 3. Memoize expensive computations
const sortedItems = useMemo(
  () => items.sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);

// 4. Memoize callbacks passed to children
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]);
```
