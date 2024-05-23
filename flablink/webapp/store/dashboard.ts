import { useUrl } from '@/utils';
import { create } from 'zustand';

export type Syncs = {
    synced: number;
    total: number;
};

export type LastCreation = {
    instrument_uid: number;
    minutes_ago: number;
};

export type HourlyData = {
    week: string;
    instrument_uid: number;
    count: number;
};

export type DailyData = {
    date: string;
    instrument_uid: number;
    count: number;
};

export type WeeklyData = {
    week: string;
    instrument_uid: number;
    count: number;
};

export type Forwarder = {
    uid: number;
    connection: "connected" | "disconnected" | "error";
    activity: "searching" | "submitting" | "idle";
    message: string;
}

export type ForwarderPerf = {
    search_started: string;
    search_ended: string;
    update_started: string;
    update_ended: string;
    message: string;
    order_uid: number
}

type DashBoardState = {    
    sync: Syncs[];
    last_creation: LastCreation[];
    last_sync: string;
    created_hourly: HourlyData[];
    created_daily: DailyData[];
    created_weekly: WeeklyData[];
    synced_hourly: HourlyData[];
    synced_daily: DailyData[];
    synced_weekly: WeeklyData[];
    forwarders: Forwarder[];
    forwarder_perf: ForwarderPerf[];
    fetchStatictics: () => Promise<void>;
    fetchForwarder: () => Promise<void>;
    fetchForwarderPerf: () => Promise<void>;
    forwarderActivity: (payload: any) => void;
};


export const useDashBoardStore = create<DashBoardState>((set) => ({
    sync: [],
    last_creation: [],
    last_sync: "",
    created_hourly: [],
    created_daily: [],
    created_weekly: [],
    synced_hourly: [],
    synced_daily: [],
    synced_weekly: [],
    forwarders: [],
    forwarder_perf: [],
    fetchStatictics: async () => {
        fetch(useUrl("/orders/stats")).then((res) => res.json()).then((data) => {
        set((state) => ({...state, ...data}));
        }).catch((err) => { console.error(err); });
    },
    fetchForwarder: async () => {
        fetch(useUrl("/forwarder")).then((res) => res.json()).then((data) => {
        set(({forwarders: data}));
        }).catch((err) => { console.error(err); });
    },
    fetchForwarderPerf: async () => {
        fetch(useUrl("/forwarder-performance")).then((res) => res.json()).then((data) => {
        set(({forwarder_perf: data}));
        }).catch((err) => { console.error(err); });
    },
    forwarderActivity: (payload: any) => {
      set((state) => ({
        forwarders: state.forwarders.map((i) => ({ ...i,  ...payload})),
      }));
    }
}));

// ask assistent to generate data for sync and creation heat maps: time of day vs day of week by instrument
