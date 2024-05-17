// src/store/keywordMappingsStore.ts
import { useUrl } from '@/utils';
import { create } from 'zustand';

type KeywordMapping = {
  uid: number;
  keyword: string;
  mappings: string;
};

type KeywordMappingsState = {
  keywordMappings: KeywordMapping[];
  addMapping: (keyword: string, mappings: string) => Promise<void>;
  updateMapping: (uid: number, keyword: string, mappings: string) => Promise<void>;
  fetchMappings: () => Promise<void>;
  deleteMapping: (uid: number) => Promise<void>;
};

export const useKeywordMappingsStore = create<KeywordMappingsState>((set) => ({
  keywordMappings: [],
  addMapping: async (keyword, mappings) => {
    fetch(useUrl('/keyword-mappings'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ keyword, mappings, is_active: true})
    }).then(res => res.json()).then(payload => {
         set((state) => ({
        ...state,
        keywordMappings: [payload, ...state.keywordMappings]
      }));
    }).catch(err => console.log(err))
  },
  updateMapping: async (uid, keyword, mappings) => {
    fetch(useUrl(`/keyword-mappings/${uid}`), {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ keyword, mappings, is_active: true})
    }).then(res => res.json()).then(payload => {
      set((state) => ({
      ...state,
      keywordMappings: state.keywordMappings.map((m) => m.uid === uid? {...m,  ...payload} : m)
      }));
     }).catch(err => console.log(err))
  },
  fetchMappings: async () => {
    fetch(useUrl('/keyword-mappings')).then(res => res.json())
    .then(mappings => set(() => ({ keywordMappings: mappings })))
    .catch(err => console.log(err))
  },
  deleteMapping: async (uid) => {
    fetch(useUrl(`/keyword-mappings/${uid}`), {
      method: 'DELETE',
      headers: {'Content-Type': 'application/json'}
    }).then(res => res.json())
    .then(() => set((state) => ({ keywordMappings: state.keywordMappings.filter((mapping) => mapping.uid !== uid) })))
    .catch(err => console.log(err))
  },
}));
