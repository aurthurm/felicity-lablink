// src/store/instrumentsStore.ts
import { useUrl } from '@/utils';
import { create } from 'zustand';

export type Instrument = {
  uid?: number | null;
  name?: string | null;
  code?: string | null;
  host?: string | null;
  port?: number | null;
  path?: string | null;
  baud_rate?: number | null;
  auto_reconnect: boolean;
  connection_type?: string | null;
  protocol_type?: string | null;
  socket_type?: string | null;
  connection?: "connecting" | "connected" | "disconnected";
  transmission?: "started" | "ended";
};

type InstrumentsState = {
  instruments: Instrument[];
  addInstrument: (instrument: Instrument) => Promise<void>;
  updateInstrument: (uid: number, instrument: Partial<Instrument>) => Promise<void>;
  fetchtInstruments: () => Promise<void>;
  deleteInstrument: (uid: number) => Promise<void>;
  instrumentActivity: (payload: any) => void;
};

export const useInstrumentsStore = create<InstrumentsState>((set) => ({
  instruments: [],
  addInstrument: async (instrument) => {
    fetch(useUrl('/instruments'), {
      method: 'post',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify(instrument),
    }).then((res) => res.json()).then((data) => {
      set((state) => ({
        instruments: [data, ...state.instruments],
      }));
    }).catch((err) => { console.error(err); });
  },
  updateInstrument: async (uid, instrument) => {
    fetch(useUrl(`/instruments/${uid}`), {
      method: 'put',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify(instrument),
    }).then((res) => res.json()).then((data) => {
      set((state) => ({
        instruments: state.instruments.map((i) => (i.uid === uid ? data : i)),
      }));
    }).catch((err) => { console.error(err); });
  },
  fetchtInstruments: async () => {
    fetch(useUrl('/instruments')).then((res) => res.json()).then((data) => {
      set({ instruments: data });
    }).catch((err) => { console.error(err); });
  },
  deleteInstrument: async (uid) => {
    fetch(useUrl(`/instruments/${uid}`), {
      method: 'delete',
    }).then(() => {
      set((state) => ({
        instruments: state.instruments.filter((i) => i.uid !== uid),
      }));
    }).catch((err) => { console.error(err); });
  },
  instrumentActivity: (payload: any) => {
    set((state) => ({
      instruments: state.instruments.map((i) => {
        if (i.uid === payload?.id) {
          return { ...i,  ...payload};
        }
        return i;
      }),
    }));
  }
}));
