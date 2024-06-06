import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Table,
  TableBody,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import LayoutAdmin from "@/components/layouts/admin";
import InstrumentTableRow from "@/components/instrument/instrument-table-row";
import InstrumentAdd from "@/components/instrument/instrument-add";
import { useInstrumentsStore } from "@/store/instruments";
import { useEffect } from "react"

function InstrumentsPage() {
  const instruments = useInstrumentsStore((state) => state.instruments)

  useEffect(() => {
    useInstrumentsStore.getState().fetchtInstruments()
  },[])

  return (
    <LayoutAdmin>
      <Card x-chunk="dashboard-06-chunk-0">
        <CardHeader >
          <div className="flex justify-between">
            <div>
              <CardTitle>Instruments.</CardTitle>
              <CardDescription>
                Manage your instruments.
              </CardDescription>
            </div>
            <InstrumentAdd /> 
          </div>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Connection Type</TableHead>
                <TableHead>Connection Details</TableHead>
                <TableHead>Protocol</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {instruments?.map((instrument) => (
                <InstrumentTableRow key={instrument.uid} instrument={instrument} />
              ))}
            </TableBody>
          </Table>
        </CardContent>
        <CardFooter>
          <div className="text-xs text-muted-foreground">
            Showing <strong>1-{instruments?.length}</strong> of <strong>{instruments?.length}</strong>{" "}
            products
          </div>
        </CardFooter>
      </Card>
  </LayoutAdmin>
  )
}

export default InstrumentsPage