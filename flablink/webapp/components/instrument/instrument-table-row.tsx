import { Button } from "@/components/ui/button"
import {
  MoreHorizontal,
} from "lucide-react"

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"

import { Badge } from "@/components/ui/badge"

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  TableCell,
  TableRow,
} from "@/components/ui/table"
import InstrumentForm from "./instrument-form"
import { Instrument } from "@/store/instruments"
import { useState } from "react"
import { useInstrumentsStore } from "@/store/instruments"
import ConfirmDialog from "../confirm"

export interface InstrumentTableRowProps {
  instrument: Instrument,
}

function InstrumentTableRow({ instrument }: InstrumentTableRowProps) {
  const [open, setOpen] = useState(false);
  const deleteInstrument = useInstrumentsStore((state) => state.deleteInstrument)
  
  return (
    <TableRow>
      <TableCell className="font-medium">
        {instrument.name}
      </TableCell>
      <TableCell>
        <Badge variant="outline">{instrument.connection_type}</Badge>
      </TableCell>
      <TableCell className="hidden md:table-cell">
        {((instrument.connection_type === 'tcpip') ? (
          <>
            <Badge variant="outline">{instrument.socket_type}</Badge>
            <Badge variant="outline">{instrument.host}:{instrument.port}</Badge>
          </>
        ) : (
          <>
            <Badge variant="outline">{instrument.path}:{instrument.baud_rate}</Badge>
          </>
        ))}
      </TableCell>
      <TableCell className="hidden md:table-cell">
      {instrument.protocol_type}
      </TableCell>
      <TableCell>
        <Dialog open={open}>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button
              aria-haspopup="true"
              size="icon"
              variant="ghost"
            >
              <MoreHorizontal className="h-4 w-4" />
              <span className="sr-only">Toggle menu</span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>Actions</DropdownMenuLabel>
            <DialogTrigger asChild>
              <DropdownMenuItem onClick={() => setOpen(true)}>update</DropdownMenuItem>
            </DialogTrigger>
            <ConfirmDialog 
              variant="ghost"
              btnClass="w-full justify-start pl-2 py-2 h-8 text-red-400 hover:text-red-400"
              action="Delete"
              question="Are you sure?"
              message={`This action will delete ${instrument.name} permanently!`}
              handleAction={() => deleteInstrument(instrument.uid!)}
            />
          </DropdownMenuContent>
        </DropdownMenu>
      
        <DialogContent className="sm:max-w-[725px]">
          <DialogHeader>
            <DialogTitle>Update {instrument?.name}</DialogTitle>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <InstrumentForm instrument={instrument} onFinished={setOpen} /> 
          </div>
        </DialogContent>
      </Dialog>
      </TableCell>
    </TableRow>
  )
}
export default InstrumentTableRow
