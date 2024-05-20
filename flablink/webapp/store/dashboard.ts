import { useUrl } from '@/utils';
import { create } from 'zustand';

type Syncs = {
    synced: number;
    total: number;
};

type LastCreation = {
    instrument_uid: number;
    minutes_ago: number;
};

type HourlyData = {
    week: string;
    instrument_uid: number;
    count: number;
};

type DailyData = {
    date: string;
    instrument_uid: number;
    count: number;
};

type WeeklyData = {
    week: string;
    instrument_uid: number;
    count: number;
};

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
    fetchStatictics: () => Promise<void>;
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
    fetchStatictics: async () => {
        fetch(useUrl("/orders/stats")).then((res) => res.json()).then((data) => {
            console.log(data);
        }).catch((err) => { console.error(err); });
    }
}));



// ask assistent to generate data for sync and creation heat maps: time of day vs day of week by instrument
