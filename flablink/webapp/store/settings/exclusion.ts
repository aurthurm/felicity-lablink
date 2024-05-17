import { useUrl } from '@/utils';
import { create } from 'zustand';

type ResultExclusion = {
  uid: number;
  result: string;
  reason: string;
};

type ResultExclusionsState = {
  resultExclusions: ResultExclusion[];
  addExclusion: (result: string, reason: string) => Promise<void>;
  updateExclusion: (uid: number, result: string, reason: string) => Promise<void>;
  fetchExclusions: () => Promise<void>;
  deleteExclusion: (uid: number) => Promise<void>;
};

export const useResultExclusionsStore = create<ResultExclusionsState>((set) => ({
  resultExclusions: [],
  addExclusion: async (result, reason) => {
    fetch(useUrl('/result-exclusions'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ result, reason})
    }).then(res => res.json()).then(payload => {
         set((state) => ({
        ...state,
        resultExclusions: [payload, ...state.resultExclusions]
      }));
    }).catch(err => console.log(err))
  },
  updateExclusion: async (uid, result, reason) => {
    fetch(useUrl(`/result-exclusions/${uid}`), {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ result, reason})
    }).then(res => res.json()).then(payload => {
      set((state) => ({
      ...state,
      resultExclusions: state.resultExclusions.map((m) => m.uid === uid? {...m,  ...payload} : m)
      }));
     }).catch(err => console.log(err))
  },
  fetchExclusions: async () => {
    fetch(useUrl('/result-exclusions')).then(res => res.json())
    .then(exclusions => set(() => ({ resultExclusions: exclusions })))
    .catch(err => console.log(err))
  },
  deleteExclusion: async (uid) => {
    fetch(useUrl(`/result-exclusions/${uid}`), {
      method: 'DELETE',
      headers: {'Content-Type': 'application/json'}
    }).then(res => res.json())
    .then(() => set((state) => ({ resultExclusions: state.resultExclusions.filter((exclusion) => exclusion.uid !== uid) })))
    .catch(err => console.log(err))
  },
}));

