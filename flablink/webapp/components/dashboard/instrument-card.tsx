import {
  Zap,
  ZapOff,
  RefreshCcw,
  Satellite
} from "lucide-react"

import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { useUrl } from "@/utils"

export default function InstrumentCard({ instrument }: any) {
    const connectInstrument = (uid: string) => {
        fetch(useUrl("/instruments/connection"), {
            method: "post",
            headers: {
                "Content-type": "application/json",
            },
            body: JSON.stringify({ uid, action: "connect" }),
        }).then((res) => res.json()).then((data) => {
            console.log(data)
        }).catch((err) => { console.error(err); });
    }

    const disconnectInstrument = (uid: string) => {
        fetch(useUrl("/instruments/connection"), {
            method: "post",
            headers: {
                "Content-type": "application/json",
            },
            body: JSON.stringify({ uid, action: "disconnect" }),
        }).then((res) => res.json()).then((data) => {
            console.log(data)
        }).catch((err) => { console.error(err); });
    }
  return (
    <Card className="w-[400px]">
      <CardHeader className="mb-0 pb-2">
        <div className="flex justify-between">
          <CardTitle className="text-slate-600">{ instrument?.name }</CardTitle>
          <div className="flex justify-start items-center gap-x-8">
            {(instrument?.connection === "disconnected") && <span className="text-red-500"><ZapOff size={24} /></span>}
            {(instrument?.connection === "connecting") && <span className="text-slate-500"><RefreshCcw size={24} /></span>}
            {(instrument?.connection === "connected") && <span className="text-green-500"><Zap size={24} /></span> }
            {(instrument?.trasmission === "started") && <span className="text-sky-500"><Satellite size={24} /></span>}
          </div>
        </div>
        <CardDescription>
          <span className="text-leading italic">
            {(instrument?.connection === "disconnected") 
            ? "Disconnected" : (instrument?.connection === "connecting")
            ? "Connecting" : (instrument?.trasmission === "started") 
            ? "Transmiting" : "Connected"}
          </span>
        </CardDescription>
      </CardHeader>
    </Card>
  )
}
