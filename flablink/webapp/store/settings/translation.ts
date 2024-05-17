import { useUrl } from '@/utils';
import { create } from 'zustand';

type ResultTranslation = {
  uid: number;
  original: string;
  translated: string;
  reason: string;
};

type ResultTranslationsState = {
  resultTranslations: ResultTranslation[];
  addTranslation: (original: string, translated: string, reason: string) => Promise<void>;
  updateTranslation: (uid: number, original: string, translated: string, reason: string) => Promise<void>;
  fetchTranslations: () => Promise<void>;
  deleteTranslation: (uid: number) => Promise<void>;
};

export const useResultTranslationsStore = create<ResultTranslationsState>((set) => ({
  resultTranslations: [],
  addTranslation: async (original, translated, reason) => {
    fetch(useUrl('/result-translations'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ original, translated, reason: reason ? reason : "Result must be reported as: " + translated })
    }).then(res => res.json()).then(payload => {
         set((state) => ({
        ...state,
        resultTranslations: [payload, ...state.resultTranslations]
      }));
    }).catch(err => console.log(err))
  },
  updateTranslation: async (uid, original, translated, reason) => {
    fetch(useUrl(`/result-translations/${uid}`), {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ original, translated, reason: reason ? reason : "Result must be reported as: " + translated})
    }).then(res => res.json()).then(payload => {
      set((state) => ({
      ...state,
      resultTranslations: state.resultTranslations.map((m) => m.uid === uid? {...m,  ...payload} : m)
      }));
     }).catch(err => console.log(err))
  },
  fetchTranslations: async () => {
    fetch(useUrl('/result-translations')).then(res => res.json())
    .then(translations => set(() => ({ resultTranslations: translations })))
    .catch(err => console.log(err))
  },
  deleteTranslation: async (uid) => {
    fetch(useUrl(`/result-translations/${uid}`), {
      method: 'DELETE',
      headers: {'Content-Type': 'application/json'}
    }).then(res => res.json())
    .then(() => set((state) => ({ resultTranslations: state.resultTranslations.filter((translated) => translated.uid !== uid) })))
    .catch(err => console.log(err))
  },
}));

