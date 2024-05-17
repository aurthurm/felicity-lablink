import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardFooter,
} from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox"
import { Input } from "@/components/ui/input"
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue,
  } from "@/components/ui/select"
import { useEffect, useState } from "react"
import { useInstrumentsStore } from "@/store/instruments"

// name: str
// code: str | None = None
// host: str | None = None
// port: int | None = None
// path: str | None = None
// baud_rate: int | None = None
// auto_reconnect: bool
// connection_type: str | None = None
// protocol_type: str | None = None
// socket_type: str | None = None


function InstrumentForm({ instrument, onFinished }: any) {
    const { addInstrument, updateInstrument } = useInstrumentsStore()

    const [uid, setUid] = useState<number|null>(null)
    const [name, setName] = useState("")
    const [code, setCode] = useState("")
    const [host, setHost] = useState("")
    const [port, setPort] = useState<number|null>(null)
    const [path, setPath] = useState("")
    const [baud_rate, setBaudRate] = useState<number|null>(null)
    const [auto_reconnect, setAutoReconnect] = useState(true)
    const [connection_type, setConnectionType] = useState("")
    const [protocol_type, setProtocolType] = useState("")
    const [socket_type, setSocketType] = useState("")

    useEffect(() => {
        if (instrument) {
            setUid(instrument.uid)
            setName(instrument.name)
            setCode(instrument.code)
            setHost(instrument.host)
            setPort(instrument.port)
            setPath(instrument.path)
            setBaudRate(instrument.baud_rate)
            setAutoReconnect(instrument.auto_reconnect)
            setConnectionType(instrument.connection_type)
            setProtocolType(instrument.protocol_type)
            setSocketType(instrument.socket_type)
        }
    }, [instrument])
 
  const toggleAutoReconnect = () => setAutoReconnect(ps => !ps)
  const handleConnectionChange = (value: string) => {
    setConnectionType(value)
    if (value == "serial") {
        setHost("")
        setPort(0)
        setSocketType("")
    } else {
        setPath("")
        setBaudRate(0)
    }
  }

  const handleSave = () => {
    if (uid) {
        updateInstrument(uid, {name, code, host, port, path, baud_rate, auto_reconnect, connection_type, protocol_type, socket_type})
    } else {
        addInstrument({name, code, host, port, path, baud_rate, auto_reconnect, connection_type, protocol_type, socket_type})
    }
    onFinished(false)
  }

  return (
        <Card x-chunk="dashboard-04-chunk-2">
          <CardContent>
            <form className="flex flex-col gap-4 mt-4">
              <div className="grid grid-cols-12 items-center">
                <label
                    htmlFor="name"
                    className="col-span-2 text-lg font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  >
                    Name
                  </label>
                <Input
                  id="name" 
                  className="col-span-8"
                  placeholder="Instrument Name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </div> 
              <div className="grid grid-cols-12 items-center">
                <label
                    htmlFor="code"
                    className="col-span-2 text-lg font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  >
                    Code
                  </label>
                <Input
                  id="code" 
                  className="col-span-8"
                  placeholder="Instrument Code"
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                />
              </div>
                <div className="grid grid-cols-12 items-center">
                    <label
                        htmlFor="connectionType"
                        className="col-span-2 text-lg font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                    >
                        Connection
                    </label>
                    <Select value={connection_type} onValueChange={handleConnectionChange}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder="Select a connection type" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                            <SelectLabel>Connections</SelectLabel>
                            <SelectItem value="serial">Serial</SelectItem>
                            <SelectItem value="tcpip">TCPIP</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                </div>
                {((connection_type == "serial") ? (<>
                    <div className="grid grid-cols-12 items-center">
                        <label
                            htmlFor="path"
                            className="col-span-2 text-lg font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                        >
                            Path
                        </label>
                        <Input
                        id="path" 
                        className="col-span-8"
                        placeholder="Path"
                        value={path}
                        onChange={(e) => setPath(e.target.value)}
                        />
                    </div>
                    <div className="grid grid-cols-12 items-center">
                        <label
                            htmlFor="baudRate"
                            className="col-span-2 text-lg font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                        >
                            Baud Rate
                        </label>
                        <Input
                        id="baudRate" 
                        type="number"
                        className="col-span-8"
                        placeholder="Baud Rate"
                        value={baud_rate ?? ""}
                        onChange={(e) => setBaudRate(+e.target.value)}
                        />
                    </div>
                </>) : (<>
                    <div className="grid grid-cols-12 items-center">
                        <label
                            htmlFor="host"
                            className="col-span-2 text-lg font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                        >
                            Host
                        </label>
                        <Input
                        id="host" 
                        className="col-span-8"
                        placeholder="Host"
                        value={host}
                        onChange={(e) => setHost(e.target.value)}
                        />
                    </div>
                    <div className="grid grid-cols-12 items-center">
                        <label
                            htmlFor="port"
                            className="col-span-2 text-lg font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                        >
                            Port
                        </label>
                        <Input
                        id="port" 
                        className="col-span-8"
                        type="number"
                        placeholder="Port"
                        value={port ?? ""}
                        onChange={(e) => setPort(+e.target.value)}
                        />
                    </div>
                    <div className="grid grid-cols-12 items-center">
                        <label
                            htmlFor="socketType"
                            className="col-span-2 text-lg font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                        >
                            Socket
                        </label>
                        <Select value={socket_type} onValueChange={setSocketType}>
                            <SelectTrigger className="w-[180px]">
                                <SelectValue placeholder="Select a sokcket type" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectGroup>
                                <SelectLabel>Sockets</SelectLabel>
                                <SelectItem value="server">Server</SelectItem>
                                <SelectItem value="client">Client</SelectItem>
                                </SelectGroup>
                            </SelectContent>
                        </Select>
                    </div>
                </>))}
                <div className="grid grid-cols-12 items-center">
                    <label
                        htmlFor="protocolType"
                        className="col-span-2 text-lg font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                    >
                        Protocol
                    </label>
                    <Select value={protocol_type} onValueChange={setProtocolType}>
                        <SelectTrigger className="w-[180px]">
                            <SelectValue placeholder="Select a protocol type" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                            <SelectLabel>Protocols</SelectLabel>
                            <SelectItem value="astm">astm</SelectItem>
                            <SelectItem value="hl7">hl7</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                </div>
                <div className="grid grid-cols-12 items-center">
                    <label
                        htmlFor="autoReconnect"
                        className="col-span-2 text-lg font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                    >
                        Reconnect
                    </label>
                    <Checkbox
                    id="autoReconnect" 
                    className="col-span-8"
                    checked={auto_reconnect}
                    onCheckedChange={toggleAutoReconnect} 
                    />
                </div>
            </form>
          </CardContent>
          <CardFooter className="border-t px-6 py-4">
            <Button onClick={handleSave}>Save</Button>
          </CardFooter>
        </Card>
  )
}

export default InstrumentForm
