import { Button } from "@/components/ui/button"

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger
} from "@/components/ui/dialog"

import InstrumentForm from "./instrument-form"
import { useState } from "react";

export interface InstrumentAddProps {
  instrument: any,
}

function InstrumentAdd() {
  const [open, setOpen] = useState(false);

  return (
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger asChild>
            <Button variant="ghost" onClick={() => setOpen(true)}>Add New</Button>
          </DialogTrigger>
      
          <DialogContent className="sm:max-w-[725px]">
            <DialogHeader>
              <DialogTitle>Add an Instrument</DialogTitle>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <InstrumentForm instrument={null}  onFinished={setOpen} /> 
            </div>
          </DialogContent>
      </Dialog>
  )
}
export default InstrumentAdd
