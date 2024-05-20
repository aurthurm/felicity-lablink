import { useUrl } from '@/utils';
import { create } from 'zustand';

export type Order = {
  order_id: string;
  test_id?: string;
  keyword: string;
  instrument?: string;
  result: string;
  result_date: string;
  unit?: string;
  comment?: string;
  is_sync_allowed: boolean;
  synced: boolean;
  sync_date?: string;
  sync_comment?: string;
  raw_message?: string;
  raw_data_uid: number;
  instrument_uid?: number;
};

type OrdersState = {
  orders: Order[];
  filterOrders: (keyword: string) => Promise<void>;
  fetchOrders: () => Promise<void>;
};

export const useOrdersStore = create<OrdersState>((set) => ({
  orders: [],
  filterOrders: async (keyword) => {
    fetch(useUrl(`/orders?keyword=${keyword}`)).then((res) => res.json()).then((data) => {
      set({ orders: data });
      return data;
    }).catch((err) => { console.error(err); });
  },
  fetchOrders: async () => {
      fetch(useUrl('/orders')).then((res) => res.json()).then((data) => {
        set({ orders: data });
      }).catch((err) => { console.error(err); });
  },
}));
