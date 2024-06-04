import {
  Zap,
  ZapOff,
  RefreshCcw,
  ShieldAlert,
  FileSearch,
  Replace
} from "lucide-react"

import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

export default function LimsCard({ forwarder }: any) {
  return (
    <Card className="w-[400px]">
      <CardHeader className="mb-0 pb-2">
        <div className="flex justify-between">
          <CardTitle className="text-slate-600">Sychroniser</CardTitle>
          <div className="flex justify-start items-center gap-x-8">
            {(forwarder?.connection === "connecting") && <span className="text-green-500"><RefreshCcw size={24} /></span> }
            {(forwarder?.connection === "disconnected") && <span className="text-red-500"><ZapOff size={24} /></span>}
            {(forwarder?.connection === "connected") && <span className="text-green-500"><Zap size={24} /></span> }
            {(forwarder?.connection === "error") && <span className="text-red-900"><ShieldAlert size={24} /></span>}
            {(forwarder?.activity === "searching") && <span className="text-sky-500"><FileSearch size={24} /></span>}
            {(forwarder?.activity === "submitting") && <span className="text-sky-500"><Replace size={24} /></span>}
          </div>
        </div>
        <CardDescription>
          <span className="text-leading italic">
            {(forwarder?.connection === "disconnected")  ? "Disconnected" 
            : (forwarder?.connection === "connecting") ? "Connecting" 
            : (forwarder?.trasmission === "searching") ? "Searching" 
            : (forwarder?.trasmission === "submitting") ? "Submitting"
            : (forwarder?.connection === "connected") ? "Connected" : forwarder?.connection}
          </span>
        </CardDescription>
      </CardHeader>
    </Card>
  )
}
