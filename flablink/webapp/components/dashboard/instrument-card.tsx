import { Button } from "@/components/ui/button"
import {
  Card,
  CardDescription,
  CardFooter,
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
    <Card className="w-[350px]">
      <CardHeader className="mb-0 pb-2">
        <CardTitle>{ instrument?.name }</CardTitle>
        <CardDescription>last transmitted 2 minutes ago</CardDescription>
      </CardHeader>
      <CardFooter className="mt-0 pt-0 flex justify-between">
        <Button variant="outline" className="pointer-events-none">Disconnected</Button>
        <Button variant="ghost" >Connect</Button>
      </CardFooter>
    </Card>
  )
}
