import {
  ListFilter,
} from "lucide-react"

import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Table,
  TableBody,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs"
import LayoutAdmin from "@/components/layouts/admin";
import InstrumentTableRow from "@/components/instrument/instrument-table-row";
import InstrumentAdd from "@/components/instrument/instrument-add";
import { useInstrumentsStore } from "@/store/instruments";
import { useEffect } from "react"

// code: str | None = None
// host: str | None = None
// port: int | None = None
// path: str | None = None
// baud_rate: int | None = None
// auto_reconnect: bool
// connection_type: str | None = None
// protocol_type: str | None = None
// socket_type: str | None  = None

function InstrumentsPage() {
  const instruments = useInstrumentsStore((state) => state.instruments)

  useEffect(() => {
    useInstrumentsStore.getState().fetchtInstruments()
  },[])

  return (
    <LayoutAdmin>
          <Tabs defaultValue="all">
            <div className="flex items-center">
              <TabsList>
                <TabsTrigger value="all">All</TabsTrigger>
                <TabsTrigger value="active">Active</TabsTrigger>
                <TabsTrigger value="draft">Draft</TabsTrigger>
                <TabsTrigger value="archived" className="hidden sm:flex">
                  Archived
                </TabsTrigger>
              </TabsList>

              <div className="ml-auto flex items-center gap-2">      
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="outline" size="sm" className="h-8 gap-1">
                      <ListFilter className="h-3.5 w-3.5" />
                      <span className="sr-only sm:not-sr-only sm:whitespace-nowrap">
                        Filter
                      </span>
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuLabel>Filter by</DropdownMenuLabel>
                    <DropdownMenuSeparator />
                    <DropdownMenuCheckboxItem checked>
                      Active
                    </DropdownMenuCheckboxItem>
                    <DropdownMenuCheckboxItem>Draft</DropdownMenuCheckboxItem>
                    <DropdownMenuCheckboxItem>
                      Archived
                    </DropdownMenuCheckboxItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </div>
            <TabsContent value="all">
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
            </TabsContent>
          </Tabs>
  </LayoutAdmin>
  )
}

export default InstrumentsPage