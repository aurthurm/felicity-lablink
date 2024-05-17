// src/store/ordersStore.ts
import { create } from 'zustand';
import axios from 'axios'; // Ensure axios is installed via npm/yarn

type Order = {
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
  listOrders: () => Promise<void>;
};

export const useOrdersStore = create<OrdersState>((set) => ({
  orders: [],
  filterOrders: async (keyword) => {
    try {
      const response = await axios.get('/api/orders/filter', { params: { keyword } }); // Adjust the URL to your API endpoint
      console.log(response.data); // Handle success response
      set(() => ({ orders: response.data }));
    } catch (error) {
      console.error(error); // Handle error
    }
  },
  listOrders: async () => {
    try {
      const response = await axios.get('/api/orders/list'); // Adjust the URL to your API endpoint
      console.log(response.data); // Handle success response
      set(() => ({ orders: response.data }));
    } catch (error) {
      console.error(error); // Handle error
    }
  },
}));
