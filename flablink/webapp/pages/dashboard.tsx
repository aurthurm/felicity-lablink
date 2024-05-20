import useWebSocket, { ReadyState } from 'react-use-websocket';
import {
  Activity,
  ArrowUpRight,
  CircleUser,
  CreditCard,
  DollarSign,
  Menu,
  Package2,
  Search,
  Users,
} from "lucide-react"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import InstrumentCard from "@/components/dashboard/instrument-card";
import LayoutAdmin from "@/components/layouts/admin";


import { useInstrumentsStore } from "@/store/instruments";
import { useDashBoardStore } from '@/store/dashboard';
import { useEffect, useState } from 'react';
import { useUrl, useWs } from '@/utils';
import { WS_CLIENT_ID } from '@/constant';

function DashBoardPage() {
  const { lastMessage } = useWebSocket(useWs(`/ws/${WS_CLIENT_ID}`));  
  const { instruments, fetchtInstruments, updateActivity } = useInstrumentsStore()
  const { fetchStatictics } = useDashBoardStore()

  useEffect(() => {
    fetchtInstruments();
    fetchStatictics();
  },[])

  useEffect(() => {
    if (lastMessage !== null) {
      updateActivity(lastMessage.data);
    }
  }, [lastMessage]);
  
  return (
    <LayoutAdmin>
      <div className="grid grid-cols-12 gap-x-4 w-full">
        <div className="col-span-12">
          <div className="grid gap-4 md:grid-cols-2 md:gap-8 lg:grid-cols-4">
            <Card x-chunk="dashboard-01-chunk-0">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Total Samples
                </CardTitle>
                <DollarSign className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">$45,231.89</div>
                <p className="text-xs text-muted-foreground">
                  +20.1% from yesterday
                </p>
              </CardContent>
            </Card>

            <Card x-chunk="dashboard-01-chunk-0">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Pending Syncing
                </CardTitle>
                <DollarSign className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">$45,231.89</div>
                <p className="text-xs text-muted-foreground">
                  +20.1% from yesterday
                </p>
              </CardContent>
            </Card>

            <Card x-chunk="dashboard-01-chunk-0">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Synced
                </CardTitle>
                <DollarSign className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">$45,231.89</div>
                <p className="text-xs text-muted-foreground">
                  +20.1% from yesterday
                </p>
              </CardContent>
            </Card>

            <Card x-chunk="dashboard-01-chunk-0">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Skipped
                </CardTitle>
                <DollarSign className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">$45,231.89</div>
                <p className="text-xs text-muted-foreground">
                  +20.1% from yesterday
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
        <div className="col-span-3 flex flex-col gap-2">
          {instruments.map((instrument) => (<InstrumentCard instrument={instrument} key={instrument.uid} />))}
        </div>
      </div>
    </LayoutAdmin>
  )
}

export default DashBoardPage
